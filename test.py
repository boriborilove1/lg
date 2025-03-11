from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_kakao_button():
    options = Options()
    # headless 모드로 실행 시 문제가 있다면, 디버깅용으로 아래 옵션을 주석 처리하세요.
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=800,600")
    
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://www.lguplus.com/login/fallback")
    print(f"[✅] {driver.current_url}에 접속 완료")
    
    # 페이지의 JavaScript가 실행되어 요소들이 로드될 시간을 줍니다.
    time.sleep(3)
    
    # 페이지 하단까지 스크롤하여 lazy-loading 요소들이 로드되도록 함
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    wait = WebDriverWait(driver, 30)
    try:
        # CSS Selector로 "카카오" alt 속성을 가진 img 요소 찾기
        button_img = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button > img[alt='카카오']")
        ))
        # img 요소의 부모인 button을 선택
        button = button_img.find_element(By.XPATH, "./..")
        print("버튼을 찾았습니다. 클릭 시도합니다.")
        wait.until(EC.element_to_be_clickable((By.XPATH, "./..")))
        button.click()
        print("버튼 클릭 성공!")
    except Exception as e:
        print("버튼을 찾거나 클릭하는 도중 오류 발생:", e)
        driver.save_screenshot("error_screenshot.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    click_kakao_button()
