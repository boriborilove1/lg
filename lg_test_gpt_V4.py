from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
import pyperclip
import time
import os

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
id = os.getenv("ID")
pw = os.getenv("PW")
kakao_id = os.getenv("KAKAO_ID")
kakao_pw = os.getenv("KAKAO_PW")
card_num = os.getenv("CARD_NUM")
card_name = os.getenv("CARD_NAME")
card_birth = os.getenv("CARD_BIRTH")
expiration_year = os.getenv("EXPIRATION_YEAR")
expiration_month = os.getenv("EXPIRATION_MONTH")
pay_amount = os.getenv("PAY_AMOUNT")

# Selenium WebDriver 설정
options = Options()

# GitHub Actions 환경이면 headless 모드 적용
if os.getenv("GITHUB_ACTIONS"):
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 크롬 드라이버 실행
driver = webdriver.Chrome(options=options)

# 유플러스 및 카카오 로그인 URL
url1 = 'https://www.lguplus.com/login'
login_url = 'https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D146968a52610c6c7a2e768d9a2443314%26state%3DKKAOLoginni9k9ta13ql2d99ukjpfu66sr7%26redirect_uri%3Dhttps%253A%252F%252Fwww.lguplus.com%252Flogin%252Fsns-login%252Fcallback%26response_type%3Dcode%26auth_tran_id%3Df8du9exmphq146968a52610c6c7a2e768d9a2443314m7zzbjys%26ka%3Dsdk%252F1.41.0%2520os%252Fjavascript%2520sdk_type%252Fjavascript%2520lang%252Fko-KR%2520device%252FWin32%2520origin%252Fhttps%25253A%25252F%25252Fwww.lguplus.com%26is_popup%3Dfalse%26through_account%3Dtrue&talk_login=hidden#login'
pay_url = 'https://www.lguplus.com/mypage/payinfo?p=1'

XPATHS = {
    "kakao_login_btn": "//img[@src='https://www.lguplus.com/static/pc-static/nmem/images/icon_kakao.png' and @alt='카카오']",
    "login_btn": '/html/body/div/div/div/main/article/div/div/form/div[4]/button[1]',
    "pay_btn": '/html/body/div[1]/div/div/main/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div[3]/button[1]',
    "pay_btn1": '#_uid_225',
    "confirm_pay_btn1": '/html/body/div[8]/div[1]/div/div/footer/button[2]',
    "confirm_pay_btn2": '/html/body/div[9]/div[1]/div/div/footer/button[2]',
    "confirm_pay_btn3": '/html/body/div[9]/div[1]/div/div/footer/div/button'
}



try:
    # 로그인 페이지 접속
    # driver.get(url1)
    # print(f"[✅] {url1}에 접속 완료")
    driver.get(login_url)
    print("[✅] 카카오 로그인 페이지에 접속 완료")
    time.sleep(2)

    # 카카오 로그인 버튼 클릭
    # time.sleep(2)
    # driver.find_element(By.XPATH, XPATHS["kakao_login_btn"]).click()
    # time.sleep(2)
    
    # 카카오 로그인 정보 입력
    for field, value in [('#loginId--1', kakao_id), ('#password--2', kakao_pw)]:
        pyperclip.copy(value)
        driver.find_element(By.CSS_SELECTOR, field).send_keys(Keys.CONTROL, 'v')
    print(f"[✅] 아이디, 비밀번호 입력완료")

    driver.find_element(By.XPATH, XPATHS["login_btn"]).click()
    print(f"[✅] 카카오 정보로 로그인 완료")
    time.sleep(3)

    # 결제 페이지 이동
    driver.get(pay_url)
    print(f"[✅] {pay_url}에 접속 완료")
    time.sleep(2)

    # 요금 바로납부 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, XPATHS["pay_btn1"]).click()
    print("[💰] 요금 납부 버튼 클릭")
    time.sleep(2)

    # 결제 정보 입력
    try:
        card_input = driver.find_element(By.ID, 'cardNo')
        pyperclip.copy(card_num)
        card_input.send_keys(Keys.CONTROL, 'v')
        print("[✅] 카드번호를 입력하였습니다.")
        time.sleep(1)
    except Exception as e:
        print(f"[❌] 카드번호 입력 실패: {e}")
        print("[✅] 카드사 자동결제 처리날이라 프로세스를 종료합니다.")
        
        driver.quit()  # 웹드라이버 종료
        exit(1)  # 프로그램 종료

    for field, value in [("cardCustName", card_name), ("cardCustbirth", card_birth)]:
        pyperclip.copy(value)
        driver.find_element(By.NAME, field).send_keys(Keys.CONTROL, 'v')

    print("[✅] 결제 정보 입력 완료")

    # 카드 유효기간 입력
    Select(driver.find_element(By.ID, 'selCardDate1')).select_by_value(expiration_year)
    Select(driver.find_element(By.ID, 'selCardDate2')).select_by_value(expiration_month)
    print("[✅] 카드 유효기간 입력 완료")

    # 결제 금액 입력
    pyperclip.copy(pay_amount)
    pay = driver.find_element(By.ID, 'displayPayAmt')
    pay.clear() ; pay.click()
    pay.send_keys(Keys.CONTROL,'v')
    print(f"[💰] 결제 금액 {pay_amount}원 입력 완료")
    time.sleep(1)


    # 일시불 선택
    Select(driver.find_element(By.ID, 'cardMonth')).select_by_value("0")
    print("[✅] 일시불 선택 완료")

    # 결제 버튼 클릭 (여러 경우 처리)
    for attempt in range(1, 4):  # 3번까지 시도
        try:
            # f string을 사용하여 attempt 값에 맞는 XPATH를 동적으로 참조
            xpath_key = f"confirm_pay_btn{attempt}"
            driver.find_element(By.XPATH, XPATHS[xpath_key]).click()
            print(f"[💳] 결제 버튼 클릭 (시도 {attempt})번째")
            time.sleep(2)
            break
        except:
            if attempt == 3:
                print("[❌] 결제 버튼 클릭 실패!")
            time.sleep(1)

    print("[🎉] 결제 완료!")

except Exception as e:
    print(f"[❗] 오류 발생: {e}")

finally:
    driver.quit()
    print("[✅] 브라우저 종료 완료")
