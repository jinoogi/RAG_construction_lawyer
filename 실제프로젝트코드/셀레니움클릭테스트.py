from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 웹드라이버 설정 (ChromeDriver 예시)
driver = webdriver.Chrome()  # 드라이버 경로 설정 필요할 수 있음

driver.get("https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246934&chrClsCd=010202&urlMode=admRulLsInfoP")
time.sleep(3)  # 페이지 로드 대기 (필요시 조정)

# "제#조"라는 텍스트가 있는 링크 찾기
try:
    link = driver.find_element(By.LINK_TEXT, "제4조제1항")  # 정확히 일치하는 텍스트로 링크 찾기
    link.click()  # 링크 클릭
    print("링크 클릭 성공")
except:
    print("링크를 찾을 수 없습니다.")
    
time.sleep(3)
driver.quit()