from 셀레니움3 import return_webcrawl

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

webcrawl_list = return_webcrawl()
# 각 문서 텍스트를 Document 객체로 변환
documents = [Document(page_content=text) for text in webcrawl_list]

# 스플릿된 문서를 OpenAIEmbeddings모델을 사용해 FAISS 벡터스토어(데이터베이스)를 생성함
vectorstore = FAISS.from_documents(documents=documents, embedding=OpenAIEmbeddings())

# 벡터스토어 뒤져볼 수 있는 리트리버(검색해주는 애) 선언
retriever = vectorstore.as_retriever()

query = "사업장 감독한테 적용되는 복장규정같은게 있나?"
retrieved_docs = retriever.get_relevant_documents(query)

print(retrieved_docs)