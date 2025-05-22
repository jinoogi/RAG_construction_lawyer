from bs4 import BeautifulSoup
import requests

# 웹 페이지 크롤링
url = "https://www.law.go.kr/LSW/admRulLinkProc.do?lsiSeq=2100000246934&lsClsCd=010202&chrClsCd=010202&joNo=0018000000&mode=2&gubun=admRul&admRulSeq=2100000246934&admRulNm=%EA%B7%BC%EB%A1%9C%EA%B0%90%EB%8F%85%EA%B4%80%20%EC%A7%91%EB%AC%B4%EA%B7%9C%EC%A0%95(%EC%82%B0%EC%97%85%EC%95%88%EC%A0%84%EB%B3%B4%EA%B1%B4)&datClsCd=010102"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# p 태그에서 순수 텍스트 추출
text_content = []
for p_tag in soup.select("div.pgroup p"):
    text_content.append(p_tag.get_text(strip=True))

# 결과를 출력하거나 원하는 형식으로 정리
result_text = "\n".join(text_content)
print(result_text)
