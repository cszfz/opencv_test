#coding=utf-8
import cv2
import numpy as np
import sys
import json

#图像地址
dirTrain='C:\\Users\\Raytine\\project\\image_train2\\'

#角度范围
angle=5
#角度间隔
step=0.5
#角度数目
step_number=int(angle/step*2+1)
#中心矩数
moments_num=7

#读取图像名字txt文件
image_train_f=open(dirTrain+'image_train.txt','r')
img_name_train=image_train_f.readline()		
img_name_train=img_name_train.strip('\n')	


f=np.empty([step_number*step_number*step_number,moments_num],dtype=float)

flag=0

while img_name_train:

	img = cv2.imread(dirTrain+img_name_train,0)
	ret,thresh = cv2.threshold(img,50,255,0)
	_,contours,hierarchy = cv2.findContours(thresh, 1, 2)
	cnt = contours[0]
	M = cv2.moments(cnt)
	f[flag]=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
	flag=flag+1
	img_name_train=image_train_f.readline()		
	img_name_train=img_name_train.strip('\n')	

image_train_f.close()
np.savetxt(dirTrain+'image_train_moments.txt',f,fmt='%f')