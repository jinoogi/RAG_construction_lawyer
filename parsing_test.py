# API 키를 환경변수로 관리하기 모듈 임포트
from dotenv import load_dotenv

# API 키 정보 로드
# 디렉토리에 .env 파일 만들고 OPENAI_API_KEY=sk-proj-XVfw4... 이런식으로 저장해놔야됨
load_dotenv()

import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 로더가 파싱할거 설정함
loader = WebBaseLoader(
    web_paths=("https://www.yna.co.kr/view/AKR20240924075800061?input=1195m",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            "p"
        )
    ),
)

# 설정한 로더로 로드함
docs = loader.load()
print(f"문서의 수: {len(docs)}")

# 비슷하게, 스플리터 설정하고 로드함
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

# 스플릿된 문서를 OpenAIEmbeddings모델을 사용해 FAISS 벡터스토어(데이터베이스)를 생성함
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

print(f"스플릿된 문서의 수: {len(splits)}")

for i, doc in enumerate(splits):
    print(f"문서 {i+1}: {doc}\n")





# # 벡터스토어 뒤져볼 수 있는 리트리버(검색해주는 애) 선언
# retriever = vectorstore.as_retriever()

# from langchain_core.prompts import PromptTemplate

# prompt = PromptTemplate.from_template(
#     """당신은 질문-답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다. 당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
# 검색된 다음 문맥(context) 을 사용하여 질문(question) 에 답하세요. 만약, 주어진 문맥(context) 에서 답을 찾을 수 없다면, 답을 모른다면 `주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
# 한글로 답변해 주세요. 단, 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.

# #Question: 
# {question} 

# #Context: 
# {context} 

# #Answer:"""
# )

# llm = ChatOpenAI(model_name="gpt-4o", temperature=0)


# # 랭체인에선 |를 파이프연산자로 사용해 객체를 차례로 파이프라인으로 연결해준다고함
# # 풀어보면, context와 question을 아까 prompt 템플릿에 끼워넣고 llm한테 물어본다음 사람이 읽을수 있는 텍스트로 파싱해줌
# rag_chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# from langchain_teddynote.messages import stream_response

# # stream 메소드는 인자를 rag_chain 첫단계로 넘겨준다고 함
# # 그래서, 인자가 들어가면 아까 설정한 파이프라인을 통해 처리되어 결과가 나옴
# answer = rag_chain.stream("어떤 이유로 중대재해법에 걸린거야??")
# stream_response(answer)