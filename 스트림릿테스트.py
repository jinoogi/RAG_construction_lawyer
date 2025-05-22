import streamlit as st
from dotenv import load_dotenv
import os
import pickle
import json
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document

# API 키 정보 로드
load_dotenv()

# 저장된 크롤링 결과 불러오기
with open("crawl_result.pkl", "rb") as file:
    main_laws, sub_laws = pickle.load(file)

# main_laws와 sub_laws를 Document 객체로 변환
documents = []
for main_law in main_laws:
    documents.append(Document(
        page_content=main_law[1],
        metadata={
            "type": main_law[0]["타입"],
            "조항명": main_law[0]["조항명"],
            "하위조항 uuid": main_law[0]["하위조항들의uuid"]
        }
    ))

# FAISS 벡터스토어 로드
vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 하위 조항 조회 함수
def get_sub_laws_by_uuid(uuids, sub_laws):
    matching_sub_laws = []
    for sub_law in sub_laws:
        sub_uuid = sub_law[0]["자신의uuid"]
        if sub_uuid in uuids:
            matching_sub_laws.append(sub_law)
    return matching_sub_laws

# 법 조항과 하위조항 통합 함수
def join_laws(query):
    output = []
    retrieved_docs = retriever.get_relevant_documents(query)
    
    for doc in retrieved_docs:
        main_law_data = {
            "조항명": doc.metadata.get("조항명", ""),
            "본문": doc.page_content,
            "하위조항들": []
        }
        
        uuids = doc.metadata.get("하위조항 uuid", [])
        matching_sub_laws = get_sub_laws_by_uuid(uuids, sub_laws)
        
        for sub_law in matching_sub_laws:
            main_law_data["하위조항들"].append({
                "하위조항": " ".join(sub_law[1])
            })
        
        output.append(main_law_data)
    
    return json.dumps(output, indent=4, ensure_ascii=False)

# Streamlit UI
st.title("법률 챗봇")
st.write("질문을 입력하세요:")

# 사용자의 질문 입력 받기
query = st.text_input("질문", "")

# 사용자가 질문을 입력한 경우
if query:
    # 조항과 하위조항을 포함한 데이터를 생성
    output = join_laws(query)

    # Prompt 작성
    prompt = f"""당신은 질문-답변(Question-Answering)을 수행하는 친절한 법률 AI 어시스턴트입니다. 당신의 임무는 주어진 법조항(Related_Law_Articles)을 기반으로 주어진 질문(question) 에 답하는 것입니다.
    검색된 다음 주어진 법조항(Related_Law_Articles) 을 사용하여 질문(question) 에 답하세요. 
    하위조항을 인용할때는 해당 법률의 어떤 내용을 인용하는지 알수 있게 답하세요
    한글로 답변해 주세요. 단, 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.

    #Question: 
    {query} 

    #Related_Law_Articles:
    {output} 

    #Answer:"""
    
    # OpenAI 모델 초기화
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    response = llm.invoke(prompt)
    
    # Streamlit에 출력
    st.write("### 답변:")
    st.write(response.content)
