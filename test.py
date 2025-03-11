from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

options = Options()
# 최신 headless 옵션 사용
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

# Linux 환경에서 chromedriver가 /usr/local/bin/chromedriver에 설치되었다고 가정
service = Service("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

XPATHS = {
    "kakao_login_btn": '/html/body/div[1]/div/div/main/div[1]/div/div[2]/div/div/div/div/section/ul[1]/li[1]/button/img'
}

url1 = 'https://www.lguplus.com/login/fallback'
driver.get(url1)
print(f"[✅] {driver.current_url}에 접속 완료")

# 요소가 나타날 때까지 명시적 대기 사용
wait = WebDriverWait(driver, 30)
button = wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS["kakao_login_btn"])))

print("버튼 클릭 전:", button.is_displayed(), button.is_enabled())
button.click()

# URL 변경 대기
WebDriverWait(driver, 30).until(EC.url_changes(url1))
print("URL 변경 및 페이지 로딩 완료!")
print(f"[✅] 현재 URL: {driver.current_url}")

time.sleep(10)
driver.quit()
