from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Chrome 드라이버 설정 (드라이버 경로를 설정해야 함)
driver = webdriver.Chrome()

# 페이지 열기
driver.get("https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246934&amp;chrClsCd=010202&amp;urlMode=admRulLsInfoP")
time.sleep(3)  # 페이지 로드 대기 (필요시 조정)

# 페이지 소스 가져오기
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# # div.pgroup 안에 있는 모든 텍스트 추출
pgroup_content = soup.select_one("div.pgroup").get_text(separator="\n", strip=True) if soup.select_one("div.pgroup") else "내용을 찾을 수 없습니다."

print(pgroup_content)
# print(soup)
# 브라우저 닫기
driver.quit()
