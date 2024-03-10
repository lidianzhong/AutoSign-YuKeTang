from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import identify
from selenium.webdriver.common.action_chains import ActionChains
import slide_verification
from PIL import Image
import datetime

driver = webdriver.Chrome()
# driver.maximize_window()


# driver.set_window_size(1722, 1034)

try:
    driver.set_page_load_timeout(10)
    print('开始加载页面')
    driver.get("https://changjiang.yuketang.cn/web?next=/v2/web/index&type=3")
except Exception as e:
    print(e)
    print('页面仍在加载，手动停止加载')
    driver.execute_script('window.stop()') #手动停止页面加载


print('修改 account-box 可见')
print('已修改 account-box')
# 找到 account-box 元素
account_box = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box")
driver.execute_script("arguments[0].style.display = 'block';", account_box)

print('已修改 account-box')
time.sleep(3)


print('点击 email')
email_click = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box > div.tab-box > div:nth-child(3)")
email_click.click()
print('已点击')
time.sleep(3)


print('开始输入账号')

# 找到 email 输入框
email_input = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box > div.content-box > div.form-box.email > div:nth-child(1) > div.input-box > div.left.box-center > input[type=email]")

# 输入文本 "123456" 到 email 输入框
email_input.send_keys("2942033733@qq.com")

print('已经输入账号')
time.sleep(3)


print('开始输入密码')

# 找到密码输入框
password_input = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box > div.content-box > div.form-box.email > div:nth-child(2) > div.input-box > div > input[type=password]")

# 输入密码 到密码输入框
password_input.send_keys("Li9765431")

print('已经输入密码')
time.sleep(3)

# 点击登录
print('点击登录')

# 找到登录按钮
login_button = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.J_wrapper.login-wraper.J_login.login_changjiang > div.wrapper-inner.clearfix > div.login-box.login-thu > div.account-box.toggle-box > div.content-box > div.submit-btn.login-btn.customMargin")

# 点击登录按钮
login_button.click()


print('已经点击登录')
time.sleep(3)


# 进入 iframe 页面
print('寻找 iframe 页面')
iframe = driver.find_element(By.ID, "tcaptcha_iframe")
driver.switch_to.frame(iframe)

print('已经转换')
time.sleep(5)


# 截取 #tcOperation 的 div 元素的屏幕截图
print('开始截图')
tc_operation_div = driver.find_element(By.ID, "tcOperation")
screenshot = tc_operation_div.screenshot_as_png
with open("screenshot.png", "wb") as file:
    file.write(screenshot)

# 裁剪掉左边50
image = Image.open("screenshot.png")
width, height = image.size
cropped_image = image.crop((100, 0, width, height))
cropped_image.save("right_half_screenshot.png")

# 截取 #slideBlock 的 div 元素的屏幕截图
print('开始截图')
slide_block_div = driver.find_element(By.ID, "slideBlock")
screenshot = slide_block_div.screenshot_as_png
with open("slide_block_screenshot.png", "wb") as file:
    file.write(screenshot)
print('已经截图')
time.sleep(3)


source = driver.find_element(By.ID, "tcaptcha_drag_thumb")
ActionChains(driver).click_and_hold(source).perform()
k=source.location['x']
print('k = ', k)

current_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
distance = identify.identify_gap("right_half_screenshot.png", "slide_block_screenshot.png", f"{current_time}.png")-k+100
print('distance = ', distance)
i = 0
while i <= distance:
        ActionChains(driver).move_by_offset(5,0).perform()
        i += 5
ActionChains(driver).release().perform()



# 当完成操作后，记得退出iframe，返回到主页面
driver.switch_to.default_content()
print('Done')


time.sleep(100)


driver.quit()

