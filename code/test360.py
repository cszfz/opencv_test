#coding=utf-8
#保存训练数据的moments特征以及对应angle标签
import cv2
import numpy as np
import sys


#图像地址
dirTrain='C:\\Users\\Raytine\\project\\image_train3\\'

#角度范围
angle=5
#角度间隔
step=0.5
#角度数目
step_number=int(angle/step*2+1)
#中心矩数
moments_num=7

angle_num=3


labels=np.empty([step_number*step_number*step_number,angle_num],dtype=float)
labels_x=np.empty([step_number*step_number*step_number,1],dtype=float)
labels_y=np.empty([step_number*step_number*step_number,1],dtype=float)
labels_z=np.empty([step_number*step_number*step_number,1],dtype=float)

features=np.empty([step_number*step_number*step_number,moments_num],dtype=float)

flag=0
#读取图像名字txt文件
image_train_f=open(dirTrain+'image_train.txt','r')
img_name_train=image_train_f.readline()		
img_name_train=img_name_train.strip('\n')	

while img_name_train:

	print(flag)

	img = cv2.imread(dirTrain+img_name_train,0)
	ret,thresh = cv2.threshold(img,50,255,0)
	_,contours,hierarchy = cv2.findContours(thresh, 1, 2)
	cnt = contours[0]
	M = cv2.moments(cnt)
	features[flag]=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
	
	xyz_train=(img_name_train.strip('.jpg')).split('_')
	x_train=float(xyz_train[0])
	y_train=float(xyz_train[1])
	z_train=float(xyz_train[2])
	labels[flag]=[x_train,y_train,z_train]
	labels_x[flag]=x_train
	labels_y[flag]=y_train
	labels_z[flag]=z_train
	flag=flag+1
	img_name_train=image_train_f.readline()		
	img_name_train=img_name_train.strip('\n')


image_train_f.close()
np.savetxt(dirTrain+'image_train_features.txt',features,fmt='%f')

np.savetxt(dirTrain+'image_train_labels.txt',labels,fmt='%f')
np.savetxt(dirTrain+'image_train_labels_x.txt',labels_x,fmt='%f')
np.savetxt(dirTrain+'image_train_labels_y.txt',labels_y,fmt='%f')
np.savetxt(dirTrain+'image_train_labels_z.txt',labels_z,fmt='%f')