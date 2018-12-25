#coding=utf-8
import cv2
import numpy as np
import sys
import json
import time
#图像地

dirTest='C:\\Users\\Raytine\\project\\test\\5\\'
dirTrain='C:\\Users\\Raytine\\project\\image_train2\\'
'''
dirTests=['C:\\Users\\Raytine\\project\\test\\0\\',
		  'C:\\Users\\Raytine\\project\\test\\1\\',
		  'C:\\Users\\Raytine\\project\\test\\2\\',
		  'C:\\Users\\Raytine\\project\\test\\3\\',
		  'C:\\Users\\Raytine\\project\\test\\4\\',
		  'C:\\Users\\Raytine\\project\\test\\5\\',
		  'C:\\Users\\Raytine\\project\\test\\6\\',
		  'C:\\Users\\Raytine\\project\\test\\7\\',
		  'C:\\Users\\Raytine\\project\\test\\8\\',
		  'C:\\Users\\Raytine\\project\\test\\9\\',
		  'C:\\Users\\Raytine\\project\\test\\10\\']
'''

#角度范围
angle=5
#角度间隔
step=0.5
#角度数目
step_number=int(angle/step*2+1)
#中心矩数
moments_num=7




#读取图像名字txt文件,保存到一个list中
image_train_f=open(dirTrain+'image_train.txt','r')
img_name_train=image_train_f.readline()		
img_name_train=img_name_train.strip('\n')	
img_train_list=[]

while img_name_train:
	img_train_list.append(img_name_train)
	img_name_train=image_train_f.readline()		
	img_name_train=img_name_train.strip('\n')	
image_train_f.close()

#将txt文件中的moments读取到矩阵f中
#矩阵F用来作中间运算
f=np.loadtxt(dirTrain+"image_train_moments.txt",delimiter=' ')
F=np.empty([step_number*step_number*step_number,moments_num],dtype=float)


while True:
	img_name_test=input('请输入图片：')
	img_name_test=img_name_test+'.jpg'

	#对不同尺寸的测试图片数据集

	img = cv2.imread(dirTest+img_name_test,0)
	
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
	for i in range(step_number*step_number*step_number):
		F[i,:]=f[i,:]-feature

	#求出曼哈顿距离最小的图片
	F=np.abs(F)
	s=np.sum(F,axis=1)
	index=np.argmin(s)
	m=np.min(s)

	#获得测试图片的预测偏转角度
	img_name_train=img_train_list[index]
	xyz_train=(img_name_train.strip('.jpg')).split('_')
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
