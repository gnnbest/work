import cv2

class Show:
	def __init__(self, square_h, square_w):
		self.square_h_ = square_h
		self.square_w_ = square_w

		cv2.namedWindow('elsfk')

	def redraw_img(self, img_map, log_map, img, y_offset, x_offset):
		for y in range(0, img_map.shape[0]):  # 行
			for x in range(0, img_map.shape[1]):  # 列
				if img_map[y, x] == 1:
					img[(y * self.square_h_):(y * self.square_h_ + self.square_h_),
					(x * self.square_w_):(x * self.square_w_ + self.square_w_)] = (255, 0, 0)
		for y in range(0, log_map.shape[0]):
			for x in range(0, log_map.shape[1]):
				if log_map[y, x] == 1:
					y_new = y + y_offset
					x_new = x + x_offset
					img[(y_new * self.square_h_):(y_new * self.square_h_ + self.square_h_),
					(x_new * self.square_w_):(x_new * self.square_w_ + self.square_w_)] = (255, 0, 0)


	def draw_line(self, img):
		s_num_h = int(img.shape[0] / self.square_h_)
		s_num_w = int(img.shape[1] / self.square_w_)
		# 画横线
		for i in range(0 + 4, s_num_h):
			cv2.line(img, (0, i * self.square_h_), (img.shape[1], i * self.square_h_), (128, 128, 128))
		# 画竖线
		for j in range(1, s_num_w):
			cv2.line(img, (j * self.square_w_, 0 + 4 * self.square_w_), (j * self.square_w_, img.shape[0]), (128, 128, 128))

	def hid_top(self, img):
		# 隐藏上端区域
		img[0:(0 + 4 * self.square_h_), 0:(0 + img.shape[1])] = 255

	def show_img(self, img_map, log_map, img, y_offset, x_offset):
		self.redraw_img(img_map, log_map, img, y_offset, x_offset)

		self.draw_line(img)

		self.hid_top(img)

	def waitkey(self, img):
		cv2.imshow('elsfk', img)
		key = cv2.waitKey(20)
		return key
