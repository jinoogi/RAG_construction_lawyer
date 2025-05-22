import requests
from bs4 import BeautifulSoup

url = "https://www.law.go.kr/DRF/lawService.do?OC=fk0545&target=admrul&ID=2100000246934&type=HTML&mobileYn="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://www.kosha.or.kr/kosha/info/noticeGuideline.do"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# HTML 내용 확인
print(soup.prettify())
