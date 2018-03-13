import numpy as np
import random


class Shape:

	def __init__(self):
		self.shape_list = Shape.get_block_shape_list(self)

	# 获取形状列表
	def get_block_shape_list(self):
		shape_list = []

		shape_I = np.array([[1, 1, 1, 1]])

		shape_O = np.array([[1, 1], [1, 1]])

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

	def get_random_shape(self):
		shape = random.choice(self.shape_list)
		return shape

	def rotate_shape(self, shape):
		new_shape = np.rot90(shape)
		return new_shape





