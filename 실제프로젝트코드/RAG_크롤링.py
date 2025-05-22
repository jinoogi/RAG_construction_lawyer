# API 키를 환경변수로 관리하기 모듈 임포트
from dotenv import load_dotenv

# API 키 정보 로드
# 디렉토리에 .env 파일 만들고 OPENAI_API_KEY=sk-proj-XVfw4... 이런식으로 저장해놔야됨
load_dotenv()

import pickle
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
import json

# 저장된 크롤링 결과 불러오기
with open("crawl_result.pkl", "rb") as file:
    _ , sub_laws = pickle.load(file)

# 스플릿된 문서를 OpenAIEmbeddings모델을 사용해 FAISS 벡터스토어(데이터베이스)를 생성함
vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# 벡터스토어 뒤져볼 수 있는 리트리버(검색해주는 애) 선언
retriever = vectorstore.as_retriever(search_kwargs={"k":2})

# 하위 조항 조회 함수
def get_sub_laws_by_uuid(uuids, sub_laws):
    matching_sub_laws = []
    for sub_law in sub_laws:
        sub_uuid = sub_law[0]["자신의uuid"]
        if sub_uuid in uuids:
            matching_sub_laws.append(sub_law)
    return matching_sub_laws


def join_laws(query):
    output = []
    retrieved_docs = retriever.get_relevant_documents(query)
    
    for doc in retrieved_docs:
        # 메인 조항 정보 수집
        main_law_data = {
            "조항명": doc.metadata.get("조항명", ""),
            "본문": doc.page_content,
            "하위조항들": []
        }
        
        # 본문 조항의 하위조항 UUID로 sub_laws 조회
        uuids = doc.metadata.get("하위조항 uuid", [])
        matching_sub_laws = get_sub_laws_by_uuid(uuids, sub_laws)
        
        # 하위 조항들 추가
        for sub_law in matching_sub_laws:
            main_law_data["하위조항들"].append({
                "하위조항": " ".join(sub_law[1])
            })
        
        # 메인 조항과 하위 조항을 포함한 데이터를 output에 추가
        output.append(main_law_data)
    
    # 보기 좋게 JSON 형식으로 포맷팅하여 반환
    return json.dumps(output, indent=4, ensure_ascii=False)

query = "나보고 올해 현장감독관을 편성하라는데, 어떤식으로 뽑아야되나?"
output = join_laws(query)
# print(output)

prompt = f"""당신은 질문-답변(Question-Answering)을 수행하는 친절한 법률 AI 어시스턴트입니다. 당신의 임무는 주어진 법조항(Related_Law_Articles)을 기반으로 주어진 질문(question) 에 답하는 것입니다.
검색된 다음 주어진 법조항(Related_Law_Articles) 을 사용하여 질문(question) 에 답하세요. 
하위조항을 인용할 때는 반드시 해당 법률의 내용과 의미를 명확히 설명하여, 사용자가 인용된 하위조항이 무엇을 규정하는지 쉽게 이해할 수 있게 하세요.
한글로 답변해 주세요. 단, 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.

#Question: 
{query} 

#Related_Law_Articles:
{output} 

#Answer:"""

# print(prompt)


llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
# 모델에 프롬프트 전달하고 답변 받기
response = llm.invoke(prompt)
print(response.content)