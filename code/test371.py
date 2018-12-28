#coding=utf-8
import cv2
import numpy as np
import sys
import json
import time
#图像地

dirTest='C:\\Users\\Raytine\\project\\test2\\'
dirTrain='C:\\Users\\Raytine\\project\\image_train4\\'


#角度范围
angle=5
#角度间隔
step=0.5
#角度数目
step_number=int(angle/step*2+1)
#中心矩数
moments_num=7


#将txt文件中的moments读取到矩阵f中
#矩阵F用来作中间运算
f_train=np.loadtxt(dirTrain+"image_train_features.txt",delimiter=' ')
l_train=np.loadtxt(dirTrain+"image_train_labels.txt",delimiter=' ')
F=np.empty([step_number*step_number*step_number,moments_num],dtype=float)


while True:
	img_name_test=input('请输入图片：')
	img_name_test=img_name_test+'.jpg'

	#对不同尺寸的测试图片数据集

	img = cv2.imread(dirTest+'2\\'+img_name_test,0)
	
	#阈值操作
	ret,thresh = cv2.threshold(img,50,255,0)

	#轮廓检测
	_,contours,hierarchy = cv2.findContours(thresh, 1, 2)
	cnt = contours[0]

	#轮廓特征矩
	M = cv2.moments(cnt)

	#归一化中心矩
	feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]

	#与模型库中的所有图片中心矩比较
	F=f_train-feature

	#求出曼哈顿距离最小的图片
	F=np.abs(F)
	s=np.sum(F,axis=1)
	index=np.argmin(s)
	m=np.min(s)

	#获得测试图片的预测偏转角度	
	xyz_train=l_train[index]
	x_train=float(xyz_train[0])
	y_train=float(xyz_train[1])
	z_train=float(xyz_train[2])

	print('预测偏转角度('+str(x_train)+','+str(y_train)+','+str(z_train)+')')

	#获得测试图片的实际偏转角度
	xyz_test=(img_name_test.strip('.jpg')).split('_')
	x_test=float(xyz_test[0])
	y_test=float(xyz_test[1])
	z_test=float(xyz_test[2])

	print('实际偏转角度('+str(x_test)+','+str(y_test)+','+str(z_test)+')')
