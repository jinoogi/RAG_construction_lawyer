import streamlit as st
import pickle
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import json
import re

# Streamlit 페이지 설정
st.set_page_config(page_title="법률 AI 챗봇", layout="wide")

# App 제목
st.title("🧑‍⚖️ 법률 AI 챗봇 - RAG 기반")

# FAISS 인덱스 로드 함수
@st.cache_resource
def load_faiss_index():
    # 절대 경로로 FAISS 인덱스 설정
    faiss_index_path = r"/Users/jeong-jinwook/civil_capstone/combined_faiss"
    return FAISS.load_local(faiss_index_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# combined_laws 로드 함수
@st.cache_resource
def load_combined_laws():
    with open("combined_laws.pkl", "rb") as file:
        return pickle.load(file)

# FAISS 인덱스 및 combined_laws 불러오기
try:
    vectorstore = load_faiss_index()
    combined_laws = load_combined_laws()
except Exception as e:
    st.error(f"데이터 로드 중 오류 발생: {str(e)}")
    st.stop()

# Retriever 설정
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 키워드 기반 하위 조항 필터링 함수 (빈도 기반 점수화)
def filter_sub_laws_by_keywords(uuids, sub_laws, query, max_count=2):
    """
    하위 조항을 UUID로 필터링하고, query 키워드와 관련성을 점수화하여 상위 max_count개의 하위 조항을 반환.
    """
    query_keywords = re.findall(r"\w+", query)  # 정규식 기반 키워드 추출
    scored_sub_laws = []

    for sub_law in sub_laws:
        sub_uuid = sub_law[0]["자신의uuid"]
        if sub_uuid in uuids:  # UUID로 필터링
            score = 0
            for content in sub_law[1]:
                for keyword in query_keywords:
                    score += content.count(keyword)  # 키워드 빈도만큼 점수 추가

            if score > 0:  # 관련성이 있는 경우만 추가
                scored_sub_laws.append((sub_law, score))

    # 점수 기준으로 정렬 후 상위 max_count개 반환
    scored_sub_laws = sorted(scored_sub_laws, key=lambda x: x[1], reverse=True)
    return [sub_law[0] for sub_law in scored_sub_laws[:max_count]]

# join_laws 함수
def join_laws(query, retriever, sub_laws):
    output = []
    retrieved_docs = retriever.get_relevant_documents(query)
    
    for doc in retrieved_docs:
        # 메인 조항 정보 수집
        main_law_data = {
            "조항명": doc.metadata.get("조항명", ""),
            "법령명": doc.metadata.get("법령명", ""),
            "본문": doc.page_content,
            "하위조항들": []
        }
        
        # 본문 조항의 하위조항 UUID로 sub_laws 조회
        uuids = doc.metadata.get("하위조항 uuid", [])
        matching_sub_laws = filter_sub_laws_by_keywords(uuids, sub_laws, query, max_count=2)  # 최대 3개 선택
        
        # 하위 조항들 추가
        for sub_law in matching_sub_laws:
            main_law_data["하위조항들"].append({
                "하위조항": " ".join(sub_law[1])
            })
        
        output.append(main_law_data)
    
    # JSON 형식으로 반환
    for law in output:
        law["본문"] = re.sub(r"<[^>]*>", "", law["본문"]).replace("\n", " ").strip()
        if "하위조항들" in law:
            for sub_law in law["하위조항들"]:
                sub_law["하위조항"] = re.sub(r"<[^>]*>", "", sub_law["하위조항"]).replace("\n", " ").strip()

    return json.dumps(output, indent=4, ensure_ascii=False)

# 모델 호출 함수
def generate_response(query, related_laws):
    prompt = f"""You are a friendly legal AI assistant performing Question-Answering tasks. Your mission is to answer the given question based on the provided legal articles (Related_Law_Articles).
Use the provided legal articles (Related_Law_Articles) to answer the given question (question).
All answers must be based on evidence, and the referenced articles must be explicitly cited at the end of each sentence.
When citing sub-articles, ensure that the content of the law being referenced is clearly identifiable.
Each sentence should be concise and start on a new line, but the overall response should be detailed and lengthy.
Answer in Korean. However, technical terms or names should not be translated and should remain as they are.

#Question:
{query}

#Related_Law_Articles:
{related_laws}

#Answer:"""
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
    response = llm.invoke(prompt)
    return response.content

# Streamlit UI
query = st.text_area("질문을 입력하세요", placeholder="예: 유해위험방지 계획서를 제출해야 하나요?")
if query:
    with st.spinner("법령을 검색 중입니다..."):
        # 관련 법령 검색
        sub_laws = []
        for law in combined_laws:
            sub_laws.extend(law["sub_laws"])
        related_laws = join_laws(query, retriever, sub_laws)
        
        # LLM을 사용해 답변 생성
        with st.spinner("답변을 생성 중입니다..."):
            response = generate_response(query, related_laws)
        
        # 결과 출력
        st.subheader("🔍 검색된 법령")
        st.json(json.loads(related_laws))
        
        st.subheader("💡 답변")
        st.write(response)