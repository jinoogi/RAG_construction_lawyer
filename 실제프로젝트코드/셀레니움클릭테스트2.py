from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 웹드라이버 설정 (ChromeDriver 예시)
driver = webdriver.Chrome()  # 드라이버 경로 설정 필요할 수 있음

driver.get("https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246934&chrClsCd=010202&urlMode=admRulLsInfoP")
time.sleep(3)  # 페이지 로드 대기 (필요시 조정)

# 제{숫자}조 패턴에 맞는 모든 링크 찾기
links = driver.find_elements(By.XPATH, "//a[contains(text(), '제') and contains(text(), '조') and text()[normalize-space()]]")
print(links)

# 찾은 모든 링크 중 "제{숫자}조" 형식의 링크만 클릭
for link in links:
    if link.text.startswith("제") and "조" in link.text:
        try:
            print(f"클릭할 링크 텍스트: {link.text}")
            link.click()  # 링크 클릭
            time.sleep(1)  # 각 클릭 사이에 대기 시간 추가 (필요에 따라 조정)
        except:
            print(f"클릭 실패: {link.text}")


time.sleep(3)
driver.quit()