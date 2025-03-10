from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
import pyperclip
import time
import os

# .env 파일 로드
load_dotenv()

# github action에서 그래픽 환경 사용을 위한 환경변수 설정
os.environ["DISPLAY"] = ":99"

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

# GitHub Actions 환경이면 Chromium 브라우저 경로 설정
if os.getenv("GITHUB_ACTIONS"):
    options.binary_location = "/usr/bin/chromium-browser"  # ✅ 브라우저 실행 파일 경로 지정
    service = Service("/usr/bin/chromedriver")  # ✅ 크롬 드라이버 실행 파일 경로 지정
    options.headless = True
else:
    options.binary_location = "/usr/bin/google-chrome"
    service = Service("/usr/bin/chromedriver")
    options.headless = False  # 로컬 테스트 시 GUI 실행

driver = webdriver.Chrome(service=service, options=options)

# # GitHub Actions 환경이면 headless 모드 적용
# if os.getenv("GITHUB_ACTIONS"):
#     options.binary_location = "/usr/bin/chromium-browser"
#     options.headless = True
# else:
#     options.headless = False  # 로컬 테스트 시 GUI 실행

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 크롬 드라이버 실행
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)  # 페이지 로드 대기 시간 설정

# 유플러스 및 카카오 로그인 URL
url1 = 'https://www.lguplus.com/login/fallback'
login_url = 'https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D146968a52610c6c7a2e768d9a2443314%26state%3DKKAOLoginni9k9ta13ql2d99ukjpfu66sr7%26redirect_uri%3Dhttps%253A%252F%252Fwww.lguplus.com%252Flogin%252Fsns-login%252Fcallback%26response_type%3Dcode%26auth_tran_id%3Df8du9exmphq146968a52610c6c7a2e768d9a2443314m7zzbjys%26ka%3Dsdk%252F1.41.0%2520os%252Fjavascript%2520sdk_type%252Fjavascript%2520lang%252Fko-KR%2520device%252FWin32%2520origin%252Fhttps%25253A%25252F%25252Fwww.lguplus.com%26is_popup%3Dfalse%26through_account%3Dtrue&talk_login=hidden#login'
pay_url = 'https://www.lguplus.com/mypage/payinfo?p=1'

XPATHS = {
    "kakao_login_btn": '//*[@id="_uid_176"]/img',
    "kakao_id_input" : '/html/body/div/div/div/main/article/div/div/form/div[1]/div/input',
    "kakao_pw_input" : '/html/body/div/div/div/main/article/div/div/form/div[2]/div/input',
    "login_btn": '/html/body/div/div/div/main/article/div/div/form/div[4]/button[1]',
    "pay_btn": '/html/body/div[1]/div/div/main/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div[3]/button[1]',
    "pay_btn1": '#_uid_225',
    "confirm_pay_btn1": '/html/body/div[8]/div[1]/div/div/footer/button[2]',
    "confirm_pay_btn2": '/html/body/div[9]/div[1]/div/div/footer/button[2]',
    "confirm_pay_btn3": '/html/body/div[9]/div[1]/div/div/footer/div/button'
}

XPATHS = {
    "kakao_login_btn": '/html/body/div[1]/div/div/main/div[1]/div/div[2]/div/div/div/div/section/ul[1]/li[1]/button/img',
    "kakao_id_input" : '/html/body/div/div/div/main/article/div/div/form/div[1]/div/input',
    "kakao_pw_input" : '/html/body/div/div/div/main/article/div/div/form/div[2]/div/input',
    "login_btn": '/html/body/div/div/div/main/article/div/div/form/div[4]/button[1]',
    "pay_btn": '/html/body/div[1]/div/div/main/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div[3]/button[1]',
    "pay_btn1": '#_uid_225',
    "confirm_pay_btn1": '/html/body/div[8]/div[1]/div/div/footer/button[2]',
    "confirm_pay_btn2": '/html/body/div[9]/div[1]/div/div/footer/button[2]',
    "confirm_pay_btn3": '/html/body/div[9]/div[1]/div/div/footer/div/button'
}
url1 = 'https://www.lguplus.com/login/fallback'
driver.get(url1)
print(f"[✅] {driver.current_url}에 접속 완료")

button = driver.find_element(By.XPATH, XPATHS["kakao_login_btn"])
print(button.is_enabled())  # 클릭 가능한지 확인
print(button.is_displayed())  # 화면에 표시되는지 확인
# driver.save_screenshot('C:/screenshot.png')

# 1️⃣ 버튼이 나타날 때까지 기다리기
# wait = WebDriverWait(driver, 60)
# button = wait.until(EC.visibility_of_element_located((By.XPATH, XPATHS["kakao_login_btn"])))
# button = wait.until(EC.visibility_of_element_located((By.XPATH, XPATHS["kakao_login_btn"])))
button = driver.find_element(By.XPATH, XPATHS["kakao_login_btn"])
button.click()

# 페이지 URL이 변경될 때까지 기다리기
WebDriverWait(driver, 30).until(EC.url_changes(driver.current_url))

print("URL이 변경되었고 페이지 로딩 완료!")

# 2️⃣ JavaScript로 클릭 (필요하면 display 변경)
# driver.execute_script("arguments[0].style.display = 'block';", button)
# driver.execute_script("arguments[0].scrollIntoView();", button)
# driver.execute_script("arguments[0].click();", button)
# print("[✅] 헤드리스 모드에서 버튼 클릭 성공")


current_url1 = driver.current_url
print(f"[✅] {current_url1}에 접속 완료")
time.sleep(10)

driver.quit()
