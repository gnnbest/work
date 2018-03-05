#-*- coding:utf-8 -*-
import cv2
import numpy as np
import random

from PIL import Image
from PIL import ImageDraw
import threading
import time
import cv2.cv



# log图填充大图
def fill_ori(img, roi_info, log_map, colour):

    shape = log_map.shape
    for j in range(0, shape[0]): #行
        for i in range(0, shape[1]):  #列
            if log_map[j, i] == 1:
               img[(j + roi_info['row_p']) * square_h : ((j + roi_info['row_p']) * square_h + square_h),
               (i + roi_info['col_p'])*square_w : ((i + roi_info['col_p']) * square_w + square_w)] = colour


def get_map_roi(shape):

    if(shape == 'I'):
        map_roi = np.zeros((1, 4), dtype=np.uint8)
        map_roi[0,0] = 1 #行列
        map_roi[0,1] = 1
        map_roi[0,2] = 1
        map_roi[0,3] = 1

    if (shape == 'S'):
        map_roi = np.zeros((2, 3), dtype=np.uint8)
        map_roi[0, 1] = 1  # 行列
        map_roi[0, 2] = 1
        map_roi[1, 0] = 1
        map_roi[1, 1] = 1

    if (shape == 'Z'):
        map_roi = np.zeros((2, 3), dtype=np.uint8)
        map_roi[0, 0] = 1  # 行列
        map_roi[0, 1] = 1
        map_roi[1, 1] = 1
        map_roi[1, 2] = 1

    if (shape == 'L'):
        map_roi = np.zeros((2, 3), dtype=np.uint8)
        map_roi[0, 0] = 1  # 行列
        map_roi[1, 0] = 1
        map_roi[1, 1] = 1
        map_roi[1, 2] = 1

    if (shape == 'J'):
        map_roi = np.zeros((2, 3), dtype=np.uint8)
        map_roi[0, 2] = 1  # 行列
        map_roi[1, 0] = 1
        map_roi[1, 1] = 1
        map_roi[1, 2] = 1

    if (shape == 'O'):
        map_roi = np.zeros((2, 2), dtype=np.uint8)
        map_roi[0, 0] = 1  # 行列
        map_roi[0, 1] = 1
        map_roi[1, 0] = 1
        map_roi[1, 1] = 1

    if (shape == 'T'):
        map_roi = np.zeros((2, 3), dtype=np.uint8)
        map_roi[0, 1] = 1  # 行列
        map_roi[1, 0] = 1
        map_roi[1, 1] = 1
        map_roi[1, 2] = 1

    return map_roi


# 检测上下碰撞
def collision_det(img_map, roi_info):
    is_pz = False

    for i in range(0, roi_info['w']):
        if(img_map[(roi_info['row_p'] + roi_info['h'] -1), (i + roi_info['col_p'])] ==  1 and
           img_map[(roi_info['row_p'] + roi_info['h'] -1 + 1), (i + roi_info['col_p'])] == 1):
            is_pz = True
            return is_pz
    return is_pz


#检测左右碰撞
def l_r_collision_det(img_map):
    can_left_move = True
    can_right_move = True
    if ((roi_info['col_p'] + roi_info['w']) >= s_num_w):
        can_right_move = False
    if(roi_info['col_p'] <= 0):
        can_left_move = False

    return can_left_move, can_right_move


def rotae_log(log_map):
    log_map_new = np.rot90(log_map)
    return log_map_new




num_time = 0

square_w = 30
square_h = 30

s_num_w = 10 #水平方格个数
s_num_h = 24 #竖直方格个数

img_w = square_w * s_num_w
img_h = square_h * s_num_h

Img = Image.new("RGB", (img_w,img_h), (255, 255, 255))

cv2.namedWindow("pic",flags = cv2.WINDOW_AUTOSIZE)
cv_image = cv2.cvtColor(np.asarray(Img),cv2.COLOR_RGB2BGR)

# 初始log映射
log_map = get_map_roi('I')

# 初始化大图映射
img_map = np.zeros((24, 10), dtype=np.uint8)

#log图在大图上的初始坐标（左下角）
init_cord = (4, 3)

row_value = 4
col_value = 3 #横坐标的初始（用键盘控制）

colour = (0, 255, 0)
down_time = 1000

while(1):

    num_time += 1
    img_tmp = cv_image.copy()
    img_map_tmp = img_map.copy()

    # log贴到大图上
    row_value = num_time + init_cord[0]
    col_value = col_value # ????

    sp = log_map.shape

    r_p = row_value - sp[0] # log在大图中的左上角的行坐标
    c_p = col_value # log在大图中的左上角的列坐标

    # 填充映射图
    img_map_tmp[r_p: (r_p + sp[0]), c_p:(c_p + sp[1])] = log_map

    # 填充原始图
    roi_info = {'row_p':r_p, 'col_p':c_p, 'h':sp[0], 'w':sp[1]}
    fill_ori(img_tmp, roi_info, log_map, colour)

    # 判断是否碰撞（重新初始化数据）
    if ((num_time < 20 and collision_det(img_map_tmp, roi_info)) or num_time >= 20):

        shape = random.choice(['I', 'S', 'Z', 'L', 'J', 'O', 'T'])
        colour = random.choice([(0, 0, 255), (255, 0, 0), (0, 255, 0)])
        log_map = get_map_roi(shape)
        num_time = 0
        cv_image = img_tmp.copy()
        img_map = img_map_tmp.copy()
        col_value = init_cord[1]
        down_time = 1000


    # 画横线
    for i in range(0 + 4, s_num_h):
        cv2.line(img_tmp, (0, i * square_h), (img_w, i * square_h), (128, 128, 128))
    # 画竖线
    for j in range(1, s_num_w):
        cv2.line(img_tmp, (j * square_w, 0 + 4 * square_w), (j * square_w, img_h), (128, 128, 128))


    # 隐藏上端区域
    img_tmp[0:(0 + 4 * square_h), 0:(0 + img_w)] = 255

    # 显示图像
    cv2.imshow("pic", img_tmp)
    key = cv2.waitKey(down_time)

    # 检测左右碰撞
    can_left_move, can_right_move = l_r_collision_det(roi_info)

    if(can_left_move and key == ord("a")):
        col_value -= 1

    if (can_right_move and key == ord("d")):
        col_value += 1

    if key == ord("s"): # 旋转
        log_map = rotae_log(log_map)

    if key == ord('j'): # 快速下落
        down_time = 10


cv2.destroyWindow("pic")