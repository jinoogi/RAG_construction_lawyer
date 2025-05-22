from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriver 설정
driver = webdriver.Chrome()
driver.get("https://www.law.go.kr/DRF/lawService.do?OC=fk0545&target=admrul&ID=2100000246934&type=HTML&mobileYn=")  # 실제 URL로 교체

print("checkpoint1")

try:
    print("checkpoint2")
    # 요소가 나타날 때까지 대기
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "제9조제2항"))
    )
    link.click()  # 요소를 찾으면 클릭하거나 다른 작업 수행
except Exception as e:
    print("checkpoint3")
    print("오류 발생:", e)
finally:
    print("checkpoint4")
    driver.quit()
