''' 법령 본문과 하위 법령을 구조화해서 반환합니다'''

from selenium import webdriver
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

    main_laws = []
    sub_laws = []

    for div in soup.select("div.pgroup"):
        # 체크칸있는 조문들이 알맹이니까 그것들만 다룰거임
        checkbox = div.select_one("input[name='joNoList']")
        # 알맹이 조문이고
        if checkbox != None:
            # 본문 조항명
            main_law_title = div.select_one("span.bl").get_text(strip=True) if div.select_one("span.bl") else "제목 없음"
            # 본문 조항의 하위조항들 담을 리스트
            my_sub_laws_uuid = []
            # 본문 조항의 내용
            main_law_content = div.get_text(separator="\n", strip=True)

            div_html = div.prettify()
            div_soup = BeautifulSoup(div_html, "html.parser")
            for link in div_soup.select("a[onclick^='javascript:fncLawPop']"):
                # 하위조항 하이퍼링크가 제#조... 이런식이면
                if '제' in link.text and '조' in link.text:  # 텍스트 필터링
                    new_uuid = uuid.uuid4()
                    my_sub_laws_uuid.append(new_uuid)
                    # 클릭
                    driver.execute_script(link['onclick'])
                    time.sleep(2)  # 하위 법조항 페이지 로드 대기}
                    # 하위법조항 내용추출
                    sub_html = driver.page_source
                    sub_soup = BeautifulSoup(sub_html, "html.parser")
                    sub_law_contents = []
                    for sub_div in sub_soup.select("div.pgroup"):
                        sub_law_content = sub_div.get_text(separator="\n", strip=True)
                        sub_law_contents.append(sub_law_content)
                    sub_laws.append([{"타입":"하위조항","자신의uuid":new_uuid},sub_law_contents])
            main_laws.append([{"타입":"본문","조항명":main_law_title,"하위조항들의uuid":my_sub_laws_uuid},main_law_content])
    # 브라우저 닫기
    driver.quit()
    return main_laws, sub_laws

main_laws, sub_laws = return_webcrawl()
print(main_laws)
print(sub_laws)