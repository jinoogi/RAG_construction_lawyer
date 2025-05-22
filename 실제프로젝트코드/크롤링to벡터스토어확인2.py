import pickle
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 저장된 크롤링 결과 불러오기
with open("crawl_result.pkl", "rb") as file:
    main_laws, sub_laws = pickle.load(file)

# 스플릿된 문서를 OpenAIEmbeddings모델을 사용해 FAISS 벡터스토어(데이터베이스)를 생성함
vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# 벡터스토어 뒤져볼 수 있는 리트리버(검색해주는 애) 선언
retriever = vectorstore.as_retriever(search_kwargs={"k":2})

query = "근로감독관이 어떤 범위까지 현장을 감독해야돼?"
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