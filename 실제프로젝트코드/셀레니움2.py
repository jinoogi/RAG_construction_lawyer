from selenium import webdriver
from bs4 import BeautifulSoup
import time

def print_webcrawl():
    # Chrome 드라이버 설정 (드라이버 경로를 설정해야 함)
    driver = webdriver.Chrome()

    # 페이지 열기
    driver.get("https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246934&chrClsCd=010202&urlMode=admRulLsInfoP")
    time.sleep(3)  # 페이지 로드 대기 (필요시 조정)

    # 페이지 소스 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 모든 div.pgroup 요소의 텍스트 추출
    pgroup_contents = [div.get_text(separator="\n", strip=True) for div in soup.select("div.pgroup")]

    # 각 pgroup 내용 출력
    if pgroup_contents:
        for content in pgroup_contents:
            print(content)
            print("\n" + "="*40 + "\n")  # 구분선 추가
    else:
        print("내용을 찾을 수 없습니다.")

    # 브라우저 닫기
    driver.quit()
