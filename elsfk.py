import numpy as np

img = np.array([[1, 0, 0, 0],
               [1, 1, 0, 0],
               [0, 0, 0, 0],
               [1, 0, 1, 1]])

add_row = img[1,:]
print add_row

img = np.delete(img, 3, 0)

print img

new = np.zeros((4,),dtype=np.uint8)
print new

#img = np.row_stack((img, new))
img = np.insert(img, 0, new, 0)

print img

















