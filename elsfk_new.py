#-*- coding:utf-8 -*-
import cv2
import numpy as np
import random
import time

from PIL import Image
from PIL import ImageDraw
import cv2.cv


def redraw_img(img_map, img):
    for y in range(0, img_map.shape[0]):  # 行
        for x in range(0, img_map.shape[1]):  # 列
            if img_map[y, x] == 1:
                img[(y * square_h):(y * square_h + square_h),
                    (x * square_w):(x * square_w + square_w)] = (255, 0, 0)


# 获取形状列表
def get_block_shape_list():

    shape_list = []

    shape_I = np.array([[1, 1, 1, 1]])

    shape_O = np.array([[1, 1],[1, 1]])

    shape_J = np.array([[0, 0, 1],
                       [1, 1, 1]])

    shape_T = np.array([[0, 1, 0],
                       [1, 1, 1]])

    shape_L = np.array([[1, 0, 0],
                       [1, 1, 1]])

    shape_Z = np.array([[1, 1, 0],
                       [0, 1, 1]])

    shape_S = np.array([[0, 1, 1],
                       [1, 1, 0]])

    shape_list.append(shape_I)
    shape_list.append(shape_O)
    shape_list.append(shape_J)
    shape_list.append(shape_T)
    shape_list.append(shape_L)
    shape_list.append(shape_Z)
    shape_list.append(shape_S)

    return shape_list

#  填充 img_map大图
def fill_img_map(img_map, log_map, (y_offset, x_offset)):
    for j in range(0, log_map.shape[0]):
        for i in range(0, log_map.shape[1]):
            img_map_tmp[j + y_offset, i + x_offset] = \
                img_map_tmp[j + y_offset, i + x_offset] or log_map[j, i]


# 检测上下碰撞和游戏是否已经结束
def collision_det(img_map, log_map, (y_offset, x_offset)):

    is_collision = False

    # 检测是否和下边缘碰撞
    if((y_offset + h_block) >= img_map.shape[0]):

        is_collision = True
        return is_collision

    # 检测是否和现有矩形框碰撞
    for i in range(0, log_map.shape[1]):

        for j in range(log_map.shape[0] -1, -1, -1):

            y = j + y_offset
            x = i + x_offset

            if(log_map[j, i] == 1):

                if(img_map[y + 1, x] == 1):

                    is_collision = True

                    return  is_collision

                break

    return is_collision


# 检测左右碰撞
def l_r_collision_det(img_map, (y_offset, x_offset, h_block, w_block)):

    can_left_move = True
    can_right_move = True
    for i in range(0, h_block):

        if (x_offset <= 0 or
                (img_map[(i + y_offset), (x_offset - 1)] == 1 and
                 img_map[(i + y_offset), (x_offset)] == 1)):

            can_left_move = False

        if ((x_offset + w_block -1 ) >= (img_map.shape[1] - 1) or
                (img_map[(i + y_offset), (x_offset + w_block - 1)] == 1 and
                 img_map[(i + y_offset), (x_offset + w_block)] == 1)):

            can_right_move = False

    return can_left_move, can_right_move


# 旋转log图
def rotae_log(log_map):
    log_map_new = np.rot90(log_map)
    return log_map_new


def delete_full_line(img_map):

    for j in range(0, img_map.shape[0]):
        sum = 0
        for i in range(0, img_map.shape[1]):
            sum += img_map[j, i]

        if sum == img_map.shape[1]:
            img_map = np.delete(img_map, j, 0)

            new_line = np.zeros((10,), dtype=np.uint8)
            img_map = np.insert(img_map, 0, new_line, 0)

    return img_map



square_w = 30
square_h = 30

s_num_w = 10 #水平方格个数
s_num_h = 24 #竖直方格个数

img_w = square_w * s_num_w
img_h = square_h * s_num_h

Img = Image.new("RGB", (img_w,img_h), (255, 255, 255))

cv2.namedWindow("pic",flags = cv2.WINDOW_AUTOSIZE)
img = cv2.cvtColor(np.asarray(Img),cv2.COLOR_RGB2BGR)


shape_list = get_block_shape_list()

# 初始log映射
log_map = random.choice(shape_list)

# 初始化大图映射
img_map = np.zeros((24, 10), dtype=np.uint8)

#log图在大图上的初始坐标（左下角）
cord_offset = {'x': 3, 'y':4}

colour = (0, 255, 0)

t_start = time.time()

time_interval = 1

while(1):

    img_tmp = img.copy()
    img_map_tmp = img_map.copy()

    w_block = log_map.shape[1]
    h_block = log_map.shape[0]

    y_offset = cord_offset['y'] - h_block # log在大图中的左上角的行坐标
    x_offset = cord_offset['x']           # log在大图中的左上角的列坐标

    # 判断旋转之后是否越界
    if y_offset < 0: y_offset = 0
    if x_offset < 0: x_offset = 0
    if (y_offset + h_block) > img_map.shape[0]:
        y_offset = img_map.shape[0] - h_block
    if (x_offset + w_block) > img_map.shape[1]:
        x_offset = img_map.shape[1] - w_block

    # 填充映射图(执行 或 运算)
    fill_img_map(img_map_tmp, log_map, (y_offset, x_offset))

    # 判断是否碰撞
    is_collision = collision_det(img_map_tmp, log_map, (y_offset, x_offset))

    if(is_collision and y_offset < 4): # game_over
        print 'game over !!!'
        break

    t_cur = time.time()

    if (t_cur - t_start) >= time_interval:
        cord_offset['y'] += 1
        t_start = t_cur

        if (is_collision):
            colour = random.choice([(0, 0, 255), (255, 0, 0), (0, 255, 0)])
            log_map = random.choice(shape_list)
            img_map = img_map_tmp.copy()
            cord_offset = {'x': 3, 'y': 4}
            time_interval = 1

            img_map = delete_full_line(img_map)

    # 画图显示
    redraw_img(img_map_tmp, img_tmp)

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
    key = cv2.waitKey(3000)

    # 检测左右碰撞
    can_left_move, can_right_move = l_r_collision_det(img_map_tmp, (y_offset, x_offset, h_block, w_block))

    if(can_left_move and key == ord("a")):
        cord_offset['x'] -= 1

    if (can_right_move and key == ord("d")):
        cord_offset['x'] += 1

    if key == ord("s"): # 旋转
        log_map = rotae_log(log_map)

    if key == ord('j'): # 快速下落
        time_interval = 0



cv2.destroyWindow("pic")