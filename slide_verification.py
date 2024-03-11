from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import cv2
import datetime


current_time = datetime.datetime.now().strftime("%Y%m%d%H%M")

def image_recognition(bg, tp):
    '''
    bg: 待识别的图片
    tp: 匹配的图片
    '''
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(bg)  # 背景图片
    tp_img = cv2.imread(tp)  # 缺口图片
    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 350)
    tp_edge = cv2.Canny(tp_img, 100, 350)
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    
    # 保存处理过的图片
    cv2.imwrite('result/process/' + f'{current_time}_bg.png', bg_pic)
    cv2.imwrite('result/process/' + f'{current_time}_tp.png', tp_pic)
    
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    # 返回缺口的左上角和右下角坐标
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    return tl, br


def draw_rectangle(img, tl, br, out):
    cv2.rectangle(img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite(out, img)
    
    
def cutting(img, tl, br, out):
    img = cv2.imread(img)
    cropped_img = img[tl[1]:br[1], br[0]:]
    cv2.imwrite(out, cropped_img)  # 保存在本地
    

def calc_gap_position():
    # # 处理缺口图片：向内裁剪10个像素
    # img = cv2.imread("slide_block_screenshot.png")
    # h, w = img.shape[:2]
    # img = img[10:h-10, 10:w-10]
    # # cv2.imwrite("slide_block_screenshot.png", img)

    # 识别拼图在背景图片中的位置
    tl, br = image_recognition("screenshot.png","slide_block_screenshot.png")
    draw_rectangle(cv2.imread("screenshot.png"), tl, br, 'result/images/' + f'{current_time}_1.png')
    # print(tl, br)
    # 对背景图片进行裁剪
    # cutting("screenshot.png", tl, br, "cut.png")
    # 在裁剪的图片中识别拼图缺口
    tl_cut, br_cut = image_recognition("cut.png","slide_block_screenshot.png")
    # 将裁剪的图片中的缺口位置转换为在原图中的位置
    tl = (tl_cut[0] + br[0], tl[1])
    br = (br_cut[0] + br[0], br[1])

    draw_rectangle(cv2.imread("screenshot.png"), tl, br, 'result/images/' + f'{current_time}_2.png')
    return tl[0]
