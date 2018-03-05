#-*- coding:utf-8 -*-
import cv2
import numpy as np


from PIL import Image
from PIL import ImageDraw
import threading
import time
import cv2.cv
num_time = 0

def fun_timer():
    global num_time
    num_time = num_time +1
    #print num_time
    global timer  #定义变量
    timer = threading.Timer(1,fun_timer)   #60秒调用一次函数
    # #定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    timer.start()    #启用定时器

timer = threading.Timer(1,fun_timer)  #首次启动
timer.start()




square_w = 20
square_h = 20

s_num_w = 10 #水平方格个数
s_num_h = 28 #竖直方格个数

img_w = square_w * s_num_w
img_h = square_h * s_num_h


roi_w = 4*square_w
roi_h = 4*square_h





def fill_ori(map_roi, angle, colour):
    #global square_w
    roi = np.zeros((roi_h, roi_w, 3), np.uint8)

    for j in range(0, 4): #行
        for i in range(0, 4):  #列
            roi[j * square_h:(j * square_h + square_h), i * square_w:(i * square_w + square_w)] = (255,255,255)
            if map_roi[j, i] == 1:
               roi[j*square_h:(j*square_h + square_h), i*square_w:(i*square_w + square_w)] = colour

    '''
    (h, w) = roi.shape[:2]
    center = (w/2, h/2)
    M = cv2.getRotationMatrix2D(center, angle, 1)
    roi_rotated = cv2.warpAffine(roi, M, (w, h))
    '''
    pil_image = Image.fromarray(cv2.cvtColor(roi,cv2.COLOR_BGR2RGB))
    pil_rotated = pil_image.rotate(angle, expand=255)
    roi_rotated = cv2.cvtColor(np.asarray(pil_rotated),cv2.COLOR_RGB2BGR)
    return roi_rotated


def get_map_roi(shape):
    map_roi = np.zeros((4, 4), dtype=np.uint8)
    if(shape == 'I'):
        map_roi[3,0] = 1 #行列
        map_roi[3,1] = 1
        map_roi[3,2] = 1
        map_roi[3,3] = 1

    if (shape == 'S'):
        map_roi[2, 1] = 1  # 行列
        map_roi[2, 2] = 1
        map_roi[3, 0] = 1
        map_roi[3, 1] = 1

    if (shape == 'Z'):
        map_roi[2, 0] = 1  # 行列
        map_roi[2, 1] = 1
        map_roi[3, 1] = 1
        map_roi[3, 2] = 1

    if (shape == 'L'):
        map_roi[1, 0] = 1  # 行列
        map_roi[2, 0] = 1
        map_roi[3, 0] = 1
        map_roi[3, 1] = 1

    if (shape == 'J'):
        map_roi[1, 1] = 1  # 行列
        map_roi[2, 1] = 1
        map_roi[3, 1] = 1
        map_roi[3, 0] = 1

    if (shape == 'O'):
        map_roi[2, 0] = 1  # 行列
        map_roi[2, 1] = 1
        map_roi[3, 0] = 1
        map_roi[3, 1] = 1

    if (shape == 'T'):
        map_roi[2, 0] = 1  # 行列
        map_roi[2, 1] = 1
        map_roi[2, 2] = 1
        map_roi[3, 1] = 1
    return map_roi


img_dic = {}
log_dic = {}

# 获取表格映射字典
def get_dic(img):
    dic = {}
    shape = img.shape
    h = shape[0] / square_h
    w = shape[1] / square_w
    for i in range(0, h):
        for j in range(0,w):
            key = (i, j)
            value = (i * square_h, j * square_w)

            dic[key] = value
    return dic


# 填充大图的映射图
def fill_img_map(img_map, log_map, top_point):
    shape = log_map.shape
    h = shape[0]
    w = shape[1]
    for i in range(0, h):
        for j in range(0,w):
            if log_map[i, j] == 1:
                img_map[top_point[0]+ i, top_point[1] + j] = 1
                #top_list.append()

#




Img = Image.new("RGB", (img_w,img_h), (255, 255, 255))

Img_draw = ImageDraw.Draw(Img)
'''
# 画横线
for i in range(0+4, s_num_h - 3):
    Img_draw.line([(0, i*square_h),(img_w, i*square_h)], (128,128,128))

# 画竖线
for j in range(1, s_num_w):
    Img_draw.line([(j*square_w,0 + roi_w),(j*square_w, img_h - roi_h)], (128,128,128))
'''

cv2.namedWindow("pic",flags = cv2.WINDOW_AUTOSIZE)
cv_image = cv2.cvtColor(np.asarray(Img),cv2.COLOR_RGB2BGR)

log_map = get_map_roi('I')
log_img = fill_ori(log_map, 0, (255,0,0))

img_map = np.zeros((28, 28), dtype=np.uint8)

#大图中每列填充最高的方块的索引
top_dic = {'0':0, '1':1, '1':1, '1':1, '0':0, '1':1, '1':1, '1':1}

while(1):
    img_tmp = cv_image.copy()

    if num_time > 24:
        num_time = 0

    # log贴到大图上
    img_roi = img_tmp[(num_time * square_h):(num_time * square_h) + roi_h, 3*square_w:(3*square_w + roi_w)]
    cv2.bitwise_and(img_roi, log_img, img_roi)

    # 判断是否碰撞
    if (num_time == 20 ):
        fill_img_map(img_map, log_map, (num_time+4 - 4 , 3))
        num_time = 0
        cv_image = img_tmp.copy()


    # 隐藏上下端区域
    img_tmp[0:(0+roi_h), 0:(0+img_w) ] = 128
    img_tmp[(24*square_h):(24 * square_h  + roi_h), 0:(0 + img_w)] = 128

    cv2.imshow("pic", img_tmp)
    cv2.imshow('img_map', img_map)
    cv2.waitKey(1)

cv2.destroyWindow("pic")












