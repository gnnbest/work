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
            if map_roi[j, i] == 1:
               roi[j*square_h:(j*square_h + square_h), i*square_w:(i*square_w + square_w)] = colour

    (h, w) = roi.shape[:2]
    center = (w/2, h/2)
    M = cv2.getRotationMatrix2D(center, angle, 1)
    roi_rotated = cv2.warpAffine(roi, M, (w, h))

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






Img = Image.new("RGB", (img_w,img_h), (255, 255, 255))

Img_draw = ImageDraw.Draw(Img)

# 画横线
for i in range(0+4, s_num_h - 3):
    Img_draw.line([(0, i*square_h),(img_w, i*square_h)], (128,128,128))

# 画竖线
for j in range(1, s_num_w):
    Img_draw.line([(j*square_w,0 + roi_w),(j*square_w, img_h - roi_h)], (128,128,128))



#Img_roi = Image.new("RGB", (roi_w, roi_h), (0,0,0))
map_roi = get_map_roi('I')
Img_roi = fill_ori(map_roi, -90, (255,0,0))

#roi_draw = ImageDraw.Draw(Img_roi)


#Img_roate = Img_roi.rotate(0)

cv2.namedWindow("pic",flags = cv2.WINDOW_AUTOSIZE)
cv_image = cv2.cvtColor(np.asarray(Img),cv2.COLOR_RGB2BGR)


while(1):
    tmp = cv_image.copy()

    if num_time > 24: num_time = 0
    tmp[(num_time * square_h):(num_time * square_h) + roi_h, 3*square_w:(3*square_w + roi_w)] = Img_roi

    # 隐藏上下端区域
    tmp[0:(0+roi_h), 0:(0+img_w) ] = 255
    tmp[(24*square_h+1):(24 * square_h + 1 + roi_h), 0:(0 + img_w)] = 255

    cv2.imshow("pic", tmp)
    cv2.waitKey(1)

cv2.destroyWindow("pic")












