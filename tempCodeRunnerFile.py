# 비슷하게, 스플리터 설정하고 로드함
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

# 스플릿된 문서를 OpenAIEmbeddings모델을 사용해 FAISS 벡터스토어(데이터베이스)를 생성함
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# 벡터스토어 뒤져볼 수 있는 리트리버(검색해주는 애) 선언
retriever = vectorstore.as_retriever(search_kwargs={"k":2})

query = "전지에서 화재가 발생한 원인이 뭐야?"
retrieved_docs = retriever.get_relevant_documents(query)

# 검색된 문서 출력
for i, doc in enumerate(retrieved_docs):
    print(f"검색된 문서 {i+1}: {doc}\n")

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    """당신은 질문-답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다. 당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
검색된 다음 문맥(context) 을 사용하여 질문(question) 에 답하세요. 만약, 주어진 문맥(context) 에서 답을 찾을 수 없다면, 답을 모른다면 `주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
한글로 답변해 주세요. 단, 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.

# #Question: 
# {question} 

# #Context: 
# {context} 

# #Answer:"""
)

# 프롬프트에 삽입될 내용 출력
formatted_prompt = prompt.format(question=query, context="\n".join([doc.page_content for doc in retrieved_docs]))
print("프롬프트에 삽입될 내용:")
print(formatted_prompt)
