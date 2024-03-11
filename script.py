from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import datetime
import os
import slide_verification


display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options=chrome_options)

current_time = datetime.datetime.now().strftime("%Y%m%d%H%M")

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '加载中 {:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

ENV = os.environ
email = ENV.get('EMAIL')
password = ENV.get('PASSWORD')

print('email:', email)
print('password:', password)

try:
    driver.set_page_load_timeout(10)
    print('开始加载雨课堂页面')
    driver.get("https://changjiang.yuketang.cn/web?next=/v2/web/index&type=3")
except Exception as e:
    print('10s 后页面仍在加载，手动停止加载')
    driver.execute_script('window.stop()') #手动停止页面加载


# 登录

print('################## 登录 ##################')


print('修改 account-box 可见', end="\r")
account_box = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box")
driver.execute_script("arguments[0].style.display = 'block';", account_box)
print('已修改 account-box        ')
countdown(3)

print('点击 email', end="\r")
email_click = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box > div.tab-box > div:nth-child(3)")
email_click.click()
print('已点击 email        ')
countdown(3)

print('输入账号', end="\r")
email_input = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box > div.content-box > div.form-box.email > div:nth-child(1) > div.input-box > div.left.box-center > input[type=email]")
email_input.send_keys(email)
print('已输入账号        ')
countdown(2)

print('输入密码', end="\r")
password_input = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box > div.content-box > div.form-box.email > div:nth-child(2) > div.input-box > div > input[type=password]")
password_input.send_keys(password)
print('已输入密码        ')
countdown(3)

print('点击登录', end="\r")
login_button = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box > div.content-box > div.submit-btn.login-btn.customMargin")
login_button.click()
print('已点击登录        ')
countdown(3)

print('################## 处理滑块验证 ##################')

print('进入 iframe 页面', end="\r")
iframe = driver.find_element(By.ID, "tcaptcha_iframe")
driver.switch_to.frame(iframe)
print('已进入 iframe 页面        ')
countdown(3)

print('截取滑块图片 1', end="\r")
tc_operation_div = driver.find_element(By.ID, "tcOperation")
screenshot = tc_operation_div.screenshot_as_png
with open("screenshot.png", "wb") as file:
    file.write(screenshot)
print('已经截图 1        ')
countdown(3)

print('截取滑块图片 2', end="\r")
slide_block_div = driver.find_element(By.ID, "slideBlock")
screenshot = slide_block_div.screenshot_as_png
with open("slide_block_screenshot.png", "wb") as file:
    file.write(screenshot)
print('已经截图 2        ')
countdown(3)

print('寻找滑块位置')
source = driver.find_element(By.ID, "tcaptcha_drag_thumb")
k=source.location['x']
print('滑块横坐标位置：', k)
countdown(2)

print('按住滑块不放')
ActionChains(driver).click_and_hold(source).perform()

print('调用 opencv 库识别滑块位置')
gap_position = slide_verification.calc_gap_position()
print('滑块位置：', gap_position)
distance = gap_position - k + 10
print('滑块移动距离：', distance)

print('移动滑块')
i = 0
while i <= distance:
        ActionChains(driver).move_by_offset(5,0).perform()
        i += 5
ActionChains(driver).release().perform()


print('################## 登录成功！ ##################')
driver.switch_to.default_content()
time.sleep(5)
driver.save_screenshot("result/login/" + f"{current_time}.png")

time.sleep(2)


try:
    print('点击上课')
    onlesson = driver.find_element(By.CSS_SELECTOR, "#app > div.viewContainer > div > div.onlesson")
    onlesson.click()
    time.sleep(2)
except Exception as e:
    print('not found')

if onlesson:
    print('found')
    onlesson.click()
    time.sleep(5)
else:
    print('not found')


print('Done')

time.sleep(2)   