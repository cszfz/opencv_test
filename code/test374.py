#coding=utf-8
import cv2
import numpy as np
import sys
import json
import time
#图像地

dirResult='test\\'
dirTrain='C:\\Users\\Raytine\\project\\image_train\\'

#角度范围
angle=5
#角度间隔
step=0.5
#角度数目
step_number=int(angle/step*2+1)
#中心矩数
moments_num=7

picName='107.jpg'
min_area=15000

#将txt文件中的moments读取到矩阵f中
#矩阵F用来作中间运算
f_train=np.loadtxt(dirTrain+"image_train_features.txt",delimiter=' ')

f_mean=np.mean(f_train, axis=0)


img=cv2.imread(dirResult+picName,0)
img_shape=img.shape
img_h=img_shape[0]
img_w=img_shape[1]
s_x=int(img_h/4)
e_x=img_h-s_x
s_y=int(img_w/6)
e_y=img_w-s_y
img_p=img[s_x:e_x,s_y:e_y]

cv2.imshow('img_p',img_p)
cv2.imwrite(dirResult+'img_p_'+picName,img_p)

#阈值操作
ret,thresh = cv2.threshold(img_p,125,255,0)

#轮廓检测
_,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, 2)

l=len(contours)
f=np.empty([l,moments_num],dtype=float)
F=np.empty([l,moments_num],dtype=float)

for i in range(l):
	cnt = contours[i]
	area = cv2.contourArea(cnt)
	if area>min_area:
		M = cv2.moments(cnt)
		feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
		f[i,:]=feature

F=f-f_mean
F=np.abs(F)
s=np.sum(F,axis=1)
index=np.argmin(s)

print(str(f[index]))

cnt = contours[index]
x,y,w,h = cv2.boundingRect(cnt)
x=x-10
y=y-10
w=w+20
h=h+20
result=img[y:y+h,x:x+w]
cv2.imshow('result',result)
cv2.imwrite(dirResult+'result_'+picName,result)
cv2.waitKey(0)

