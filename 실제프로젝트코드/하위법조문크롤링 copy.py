from bs4 import BeautifulSoup
import requests

# 웹 페이지 크롤링
url = "https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246934&amp;chrClsCd=010202&amp;urlMode=admRulLsInfoP"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

print(soup)

# p 태그에서 순수 텍스트 추출
text_content = []
for p_tag in soup.select("div.pgroup p"):
    text_content.append(p_tag.get_text(strip=True))

# 결과를 출력하거나 원하는 형식으로 정리
result_text = "\n".join(text_content)
print(result_text)
