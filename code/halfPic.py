#coding=utf-8
import cv2
import copy
picDir='test\\053.jpg'

img=cv2.imread(picDir)


shape = img.shape
print(shape)
dst=img[0:shape[0],int(shape[1]/2):shape[1]]
cv2.imshow('flip',dst)
cv2.imwrite('052.jpg',dst)