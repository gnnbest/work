import numpy as np
import cv2
from shape import Shape
import time
import random
from show import Show
from PIL import Image

class Game:

	def __init__(self, rows, cols, square_h, square_w): # 24/10
		self.rows_ = rows
		self.cols_ = cols

		self.square_h_ = square_h
		self.square_w_ = square_w

		self.shape_ = Shape()

		self.down_time_interval_ = 1
		self.t_start_ = time.time() # 游戏开始时间
		self.cord_offset_ = {'x': 3, 'y':4} # 初始偏移坐标

		self.img_map_ = np.zeros((self.rows_, self.cols_), dtype=np.uint8)
		self.log_map_ = self.shape_.get_random_shape()

		self.is_gameover_ = False

		self.show_ = Show(self.square_h_, self.square_w_)


	def delete_full_line(self, img_map):

		for j in range(0, img_map.shape[0]):
			sum = 0
			for i in range(0, img_map.shape[1]):
				sum += img_map[j, i]

			if sum == img_map.shape[1]:
				img_map = np.delete(img_map, j, 0)

				new_line = np.zeros((10,), dtype=np.uint8)
				img_map = np.insert(img_map, 0, new_line, 0)

		return img_map


	#  填充 img_map大图
	def fill_img_map(self, img_map, log_map, y_offset, x_offset):
		for j in range(0, log_map.shape[0]):
			for i in range(0, log_map.shape[1]):
				img_map[j + y_offset, i + x_offset] = \
					img_map[j + y_offset, i + x_offset] or log_map[j, i]


	# 检测上下碰撞和游戏是否已经结束
	def collision_det(self, img_map, log_map, y_offset, x_offset):

		is_collision = False

		# 检测是否和下边缘碰撞
		if ((y_offset + log_map.shape[0]) >= img_map.shape[0]):
			is_collision = True
			return is_collision

		# 检测是否和现有矩形框碰撞
		for i in range(0, log_map.shape[1]):

			for j in range(log_map.shape[0] - 1, -1, -1):

				y = j + y_offset
				x = i + x_offset

				if (log_map[j, i] == 1):

					if (img_map[y + 1, x] == 1):
						is_collision = True

						return is_collision

					break

		return is_collision


	# 检测左右碰撞
	def l_r_collision_det(self, img_map, log_map, y_offset, x_offset):

		can_left_move = True
		can_right_move = True
		for j in range(0, log_map.shape[0]):

			for i in range(0, log_map.shape[1]):
				if log_map[j, i] == 1:
					y = j + y_offset
					x = i + x_offset
					if (x - 1) < 0:
						can_left_move = False
					if (x + 1) > img_map.shape[1] - 1:
						can_right_move = False
					elif (img_map[y, x - 1] == 1):
						can_left_move = False
					elif (img_map[y, x + 1] == 1):
						can_right_move = False

		return can_left_move, can_right_move


	# 判断旋转之后是否越界
	def deal_border(self, y_offset, x_offset, log_map_shape, img_map_shape):
		h_block = log_map_shape[0]
		w_block = log_map_shape[1]
		h_img = img_map_shape[0]
		w_img = img_map_shape[1]
		if y_offset < 0: y_offset = 0
		if x_offset < 0: x_offset = 0
		if (y_offset + h_block) > h_img:
			y_offset = h_img - h_block
		if (x_offset + w_block) > w_img:
			x_offset = w_img - w_block

		return y_offset, x_offset


	def run(self):
		Img = Image.new("RGB", (self.square_w_ * self.cols_, self.square_h_ * self.rows_), (255, 255, 255))
		img = cv2.cvtColor(np.asarray(Img), cv2.COLOR_RGB2BGR)

		while (1):
			img_tmp = img.copy()

			w_block = self.log_map_.shape[1]
			h_block = self.log_map_.shape[0]

			y_offset = self.cord_offset_['y'] - h_block  # log在大图中的左上角的行坐标
			x_offset = self.cord_offset_['x']  # log在大图中的左上角的列坐标

			y_offset, x_offset = \
				self.deal_border(y_offset, x_offset, self.log_map_.shape, self.img_map_.shape)

			# 判断是否碰撞
			is_collision = self.collision_det(self.img_map_, self.log_map_, y_offset, x_offset)

			if (is_collision and y_offset < 4):  # game_over
				self.is_gameover_ = True
				print('game over !!!')
				break
				return self.is_gameover_

			t_cur = time.time()

			if (t_cur - self.t_start_) >= self.down_time_interval_:
				self.cord_offset_['y'] += 1
				self.t_start_ = t_cur

				if (is_collision):
					self.fill_img_map(self.img_map_, self.log_map_, y_offset, x_offset)
					self.log_map_ = self.shape_.get_random_shape()

					self.cord_offset_ = {'x': 3, 'y': 4}
					self.down_time_interval_ = 1
					self.img_map_ = self.delete_full_line(self.img_map_)
					continue

			self.show_.show_img(self.img_map_, self.log_map_, img_tmp, y_offset, x_offset)

			key = self.show_.waitkey(img_tmp)

			# 检测左右碰撞
			can_left_move, can_right_move = self.l_r_collision_det(self.img_map_, self.log_map_, y_offset, x_offset)

			if (can_left_move and key == ord("a")):
				self.cord_offset_['x'] -= 1

			if (can_right_move and key == ord("d")):
				self.cord_offset_['x'] += 1

			if key == ord("s"):  # 旋转
				self.log_map_ = self.shape_.rotate_shape(self.log_map_)

			if key == ord('j'):  # 快速下落
				self.down_time_interval_ = 0






















