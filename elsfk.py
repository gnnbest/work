#-*- coding:utf-8 -*-
import cv2
import numpy as np


from PIL import Image
from PIL import ImageDraw
import threading
import time

num_time = 0

def fun_timer():
    global num_time
    num_time = num_time +1
    print num_time
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



Img = Image.new("RGB", (img_w,img_h), (255, 255, 255))

Img_draw = ImageDraw.Draw(Img)

# 画横线
for i in range(0+4, s_num_h - 3):
    Img_draw.line([(0, i*square_h),(img_w, i*square_h)], (128,128,128))

# 画竖线
for j in range(1, s_num_w):
    Img_draw.line([(j*square_w,0 + roi_w),(j*square_w, img_h - roi_h)], (128,128,128))



Img_roi = Image.new("RGB", (roi_w, roi_h), (0,0,0))

roi_draw = ImageDraw.Draw(Img_roi)

#for i in range(0, 4):
#    roi_draw.line([(0, i*square_h),(4*square_w, i*square_h)], (128,0,0))

#for j in range(0, 4):
#    roi_draw.line([(j*square_w,0),(j*square_w, 4*square_h)], (128,0,0))

#roi_draw.line([(0, 40 + 80),(80, 40 + 80)], (256,0,0))
Img_roate = Img_roi.rotate(90)

cv2.namedWindow("pic",flags = cv2.WINDOW_AUTOSIZE)
cv_image = cv2.cvtColor(np.asarray(Img),cv2.COLOR_RGB2BGR)

cover_img = np.zeros((roi_h, img_w,3), dtype=np.uint8)
cover_img = 255

while(1):
    tmp = cv_image.copy()

    if num_time > 24: num_time = 0
    tmp[(num_time * square_h):(num_time * square_h) + roi_h, 60:(60 + roi_w)] = Img_roate

    # 隐藏上下端区域
    tmp[0:(0+roi_h), 0:(0+img_w) ] = cover_img
    tmp[(24*square_h+1):(24 * square_h + 1 + roi_h), 0:(0 + img_w)] = cover_img

    cv2.imshow("pic", tmp)
    cv2.waitKey(1)

cv2.destroyWindow("pic")












