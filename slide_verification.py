import cv2
from PIL import Image

def identify_gap(bg, tp, out):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    param_cut = 100
    
    # 将背景图片裁剪掉左边 param_cut 个像素
    full_img = Image.open(bg)
    width, height = full_img.size
    cropped_image = full_img.crop((param_cut, 0, width, height))
    cropped_image.save("cropped_image.png")
    
    
    # 读取背景图片和缺口图片
    cropped_img = cv2.imread('cropped_image.png')  # 右边背景图片
    bg_img = cv2.imread(bg)                  # 背景图片
    tp_img = cv2.imread(tp)                  # 缺口图片
    # 识别图片边缘
    cropped_edge = cv2.Canny(cropped_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    # 转换图片格式
    cropped_pic = cv2.cvtColor(cropped_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    # 缺口匹配
    res = cv2.matchTemplate(cropped_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = (max_loc[0] + param_cut, max_loc[1])  # 左上角点的坐标
    br = (tl[0] + tw + param_cut, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite('result/images' + out, bg_img)  # 保存在本地
    # 返回缺口的X坐标
    return tl[0]

def identify_gap_1(bg, tp, out):
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
    
    # 切片为右半部分
    width = bg_pic.shape[1]
    bg_pic = bg_pic[:, :width//2]
    
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite(out, bg_img)  # 保存在本地
    print(tl[0])
    # 返回缺口的X坐标
    return tl[0] + width//2