''' 법령 본문과 하위 법령을 구조화해서 반환합니다- 미완'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def return_webcrawl():
    # Chrome 드라이버 설정 (드라이버 경로를 설정해야 함)
    driver = webdriver.Chrome()

    # 페이지 열기
    driver.get("https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246934&chrClsCd=010202&urlMode=admRulLsInfoP")
    time.sleep(3)  # 페이지 로드 대기 (필요시 조정)

    # 페이지 소스 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # # 모든 div.pgroup 요소의 텍스트 추출
    # pgroup_contents = [div.get_text(separator="\n", strip=True) for div in soup.select("div.pgroup")]

    pgroup_contents = []
    text = []
    title = []

    for div in soup.select("div.pgroup"):
        # div.pgroup 내에 name="joNoList"인 input 요소가 있는지 확인
        checkbox = div.select_one("input[name='joNoList']")
        if checkbox != None:
            pgroup_contents.append(div)
            text.append(div.get_text(separator="\n", strip=True))
            title.append(div.select_one("span.bl").get_text(strip=True) if div.select_one("span.bl") else "제목 없음")
    # 브라우저 닫기
    driver.quit()

    return pgroup_contents, text, title

pgroup_contents, text, title = return_webcrawl()
for index,a in enumerate(title):
    print(a)
    print(text[index])
    print()
