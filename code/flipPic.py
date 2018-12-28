#coding=utf-8
import cv2
import copy
picDir='D:\\test2.jpg'

img=cv2.imread(picDir)

dst=copy.deepcopy(img)
shape = img.shape
print(shape)
for i in range(shape[0]):
	for j in range(shape[1]):
		dst[i][j]=img[i][shape[1]-j-1]
cv2.imshow('flip',dst)
cv2.imwrite('D:\\testflip.jpg',dst)