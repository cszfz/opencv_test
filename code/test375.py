#coding=utf-8
import cv2
import numpy as np
import sys
import json
import time
#图像地

dirTest='test\\'
dirResult='result\\th2\\'
dirTrain='C:\\Users\\Raytine\\project\\image_train\\'
picNames=['045.jpg','054.jpg','107.jpg','128.jpg']
#picNames=['015.jpg','021.jpg','025.jpg','029.jpg','045.jpg','053.jpg','059.jpg','107.jpg','128.jpg']

#中心矩数
moments_num=7


min_area=15000

#将txt文件中的moments读取到矩阵f中
#矩阵F用来作中间运算
f_train=np.loadtxt(dirTrain+"image_train_features.txt",delimiter=' ')
F=np.empty(f_train.shape,dtype=float)
f_mean=np.mean(f_train, axis=0)

for picName in picNames:

	#读取图片
	img=cv2.imread(dirTest+picName,0)

	#阈值操作
	#ret,thresh = cv2.threshold(img,125,255,0)
	thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	#thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	
	#轮廓检测
	_,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, 2)

	l=len(contours)
	f=np.empty([l,moments_num],dtype=float)
	
	for i in range(l):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		if area>min_area:
			M = cv2.moments(cnt)
			feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
			f[i,:]=feature

	f=f-f_mean
	f=np.abs(f)
	s=np.sum(f,axis=1)
	index=np.argmin(s)
	print(str(f[index]))
	cnt = contours[index]
	x,y,w,h = cv2.boundingRect(cnt)
	x=x-10
	y=y-10
	w=w+20
	h=h+20
	result=img[y:y+h,x:x+w]
	#cv2.imshow('result',result)
	cv2.imwrite(dirResult+'result_'+picName,result)


