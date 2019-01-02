#coding=utf-8
#保存训练数据的moments特征以及对应angle标签
import cv2
import numpy as np
import sys


#图像地址
dirTrain='C:\\Users\\Raytine\\project\\image_train\\'



img = cv2.imread(dirTrain+'10.0_-10_-2.2.jpg',0)
ret,thresh = cv2.threshold(img,50,255,0)
#thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,1)
#thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

cv2.imwrite('thresh.jpg',thresh)

cnt = contours[0]
img=cv2.imread(dirTrain+'10.0_-10_-2.2.jpg')
img = cv2.drawContours(img, contours, -1, (255,0,0), 1)
cv2.imwrite('contous1.jpg',img)
M = cv2.moments(cnt)
features=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]

print(str(features))