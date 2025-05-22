import pickle
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# 저장된 크롤링 결과 불러오기
with open("crawl_result.pkl", "rb") as file:
    main_laws, sub_laws = pickle.load(file)

# main_laws와 sub_laws를 Document 객체로 변환
documents = []

# main_laws 처리
for main_law in main_laws:
    documents.append(Document(
        page_content=main_law[1],  # 본문 내용
        metadata={
            "type": main_law[0]["타입"],
            "조항명": main_law[0]["조항명"],
            "하위조항 uuid": main_law[0]["하위조항들의uuid"]
        }
    ))

# 스플릿된 문서를 OpenAIEmbeddings모델을 사용해 FAISS 벡터스토어(데이터베이스)를 생성함
vectorstore = FAISS.from_documents(documents=documents, embedding=OpenAIEmbeddings())

# FAISS 인덱스 저장
vectorstore.save_local("faiss_index")

# 벡터스토어 뒤져볼 수 있는 리트리버(검색해주는 애) 선언
retriever = vectorstore.as_retriever(search_kwargs={"k":2})

query = "지금 우리 현장에서 작업자 한명이 추락해서 중태인데 상부에 어떻게 보고해야하나?"
retrieved_docs = retriever.get_relevant_documents(query)

# 하위 조항 조회 함수
def get_sub_laws_by_uuid(uuids, sub_laws):
    matching_sub_laws = []
    for sub_law in sub_laws:
        sub_uuid = sub_law[0]["자신의uuid"]
        if sub_uuid in uuids:
            matching_sub_laws.append(sub_law)
    return matching_sub_laws

for doc in retrieved_docs:
    print("본문:", doc.page_content)
    print("메타데이터:", doc.metadata)

    # 본문 조항의 하위조항 UUID로 sub_laws 조회
    uuids = doc.metadata.get("하위조항 uuid", [])
    matching_sub_laws = get_sub_laws_by_uuid(uuids, sub_laws)
    
    # 하위조항 내용 출력
    for sub_law in matching_sub_laws:
        print("\n하위조항:", " ".join(sub_law[1]))  # 하위 조항의 내용들 출력
        print("하위조항 메타데이터:", sub_law[0])
    print("- "*100)