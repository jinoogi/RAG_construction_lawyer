''' 본문 하위조항 순회 클릭 테스트'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import uuid

def return_webcrawl():
    # Chrome 드라이버 설정 (드라이버 경로를 설정해야 함)
    driver = webdriver.Chrome()

    # 페이지 열기
    driver.get("https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246934&chrClsCd=010202&urlMode=admRulLsInfoP")
    time.sleep(3)  # 페이지 로드 대기 (필요시 조정)

    # 페이지 소스 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    pgroup_contents = []
    text = []
    title = []

    for div in soup.select("div.pgroup"):
        sub_laws = []

        # 체크칸있는 조문들이 알맹이니까 그것들만 다룰거임
        checkbox = div.select_one("input[name='joNoList']")
        if checkbox != None:
            pgroup_contents.append(div)
            text.append(div.get_text(separator="\n", strip=True))
            title.append(div.select_one("span.bl").get_text(strip=True) if div.select_one("span.bl") else "제목 없음")

            # div 안의 하위조항을 클릭하고 다루는 코드
            div_html = div.prettify()
            div_soup = BeautifulSoup(div_html, "html.parser")
            for link in div_soup.select("a[onclick^='javascript:fncLawPop']"):
                print(link.text)
                if '제' in link.text and '조' in link.text:  # 텍스트 필터링
                        new_uuid = uuid.uuid4()
                        # JavaScript 함수를 실행하여 링크 클릭
                        driver.execute_script(link['onclick'])
                        time.sleep(2)  # 하위 법조항 페이지 로드 대기}
                        sub_laws.append(new_uuid)
        print(sub_laws)
    # 브라우저 닫기
    driver.quit()

    return pgroup_contents, text, title

pgroup_contents, text, title = return_webcrawl()
