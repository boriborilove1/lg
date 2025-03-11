from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_kakao_button():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Ubuntu 환경에서 apt-get으로 설치된 chromedriver 경로
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://www.lguplus.com/login/fallback")
    print(f"[✅] {driver.current_url}에 접속 완료")
    
    # 페이지가 로드될 시간을 주기 위해 잠시 대기
    time.sleep(2)
    
    # 페이지 스크롤: lazy-loading 요소가 로드되도록 전체 페이지를 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    wait = WebDriverWait(driver, 30)
    try:
        # 해당 버튼이 존재할 때까지 대기
        button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[img[@alt='카카오']]")))
        # 버튼이 클릭 가능한 상태가 될 때까지 추가 대기
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[img[@alt='카카오']]")))
        button.click()
        print("버튼 클릭 성공!")
    except Exception as e:
        print("버튼을 찾거나 클릭하는 도중 오류 발생:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    click_kakao_button()
