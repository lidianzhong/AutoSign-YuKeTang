from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import cv2

def identify_gap(bg, tp, out):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(bg)  # 背景图片
    tp_img = cv2.imread(tp)  # 缺口图片
    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite('result/images' + out, bg_img)  # 保存在本地
    print(tl[0])
    # 返回缺口的X坐标
    return tl[0]


# # identify_gap("result1.png","result2.png","1.png")
# chome_option=webdriver.ChromeOptions()
# driver=webdriver.Chrome()
# driver.get("https://spcjsample.gsxt.gov.cn/index.php?m=Admin&c=Sample&a=receiveOrEditSample&oper_type=receive&sample_code=XC21320115216735911")
# # driver.maximize_window()
# driver.find_element_by_xpath('//*[@id="formReceiveSample"]/div[2]/span').click()
# time.sleep(3)
# source=driver.find_element_by_xpath('//*[@id="tncode_div"]/div[5]/div[1]')
# target=driver.find_element_by_xpath('//*[@id="tncode_div"]/canvas[2]')
# time.sleep(2)
# k=source.location['x']
# print(k)
# ActionChains(driver).click_and_hold(source).perform()

# driver.save_screenshot('result.png')#这里截全屏，截全屏后再保存，之后再截图

# # im = cv2.imread('result.png')
# # sp = im.shape
# # sz1 = sp[0]
# # sz2 = sp[1]
# # sz3 = sp[2]
# # im = im[(int(sz1)//2-119):(int(sz1)//2+31),(int(sz2)//2-130):(int(sz2)//2+115)]
# # cv2.imwrite('result1.png',im)
# distance = identify_gap("result.png","result2.png","1.png")-k
# print(distance)
# i = 0
# while i <= distance:
#         ActionChains(driver).move_by_offset(5,0).perform()
#         i += 5
# ActionChains(driver).release().perform()
# time.sleep(3)
# driver.quit()

