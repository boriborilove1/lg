from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_kakao_button():
    # Chrome 옵션 설정 (headless 모드 포함)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Ubuntu 환경에서 apt-get 설치된 chromedriver 경로 (예: /usr/bin/chromedriver)
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    # URL에 접속 (예: LG U+ 로그인 페이지만 사용)
    driver.get("https://www.lguplus.com/login/fallback")
    print(f"현재 URL: {driver.current_url}")
    
    # 명시적 대기를 통해 alt 속성이 '카카오'인 img를 포함하는 버튼이 클릭 가능해질 때까지 기다립니다.
    wait = WebDriverWait(driver, 30)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[img[@alt='카카오']]")))
    
    # 버튼 상태 확인 및 클릭
    if button.is_displayed() and button.is_enabled():
        print("버튼을 클릭합니다.")
        button.click()
        print("버튼 클릭 완료!")
    else:
        print("버튼이 표시되지 않거나 클릭할 수 없습니다.")
    
    driver.quit()

if __name__ == "__main__":
    click_kakao_button()
