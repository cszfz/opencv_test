#coding=utf-8
import cv2
import numpy as np
import sys
import json
import time


dirTrain='C:\\Users\\Raytine\\project\\image_train\\'

#角度范围
angle=5
#角度间隔
step=0.2
#角度数目
step_number=int(angle/step*2+1)

angle_num=3


labels=np.empty([step_number*step_number*step_number,angle_num],dtype=float)
labels_x=np.empty([step_number*step_number*step_number,1],dtype=float)
labels_y=np.empty([step_number*step_number*step_number,1],dtype=float)
labels_z=np.empty([step_number*step_number*step_number,1],dtype=float)
flag=0

#读取图像名字txt文件,保存到一个list中
image_train_f=open(dirTrain+'image_train.txt','r')
img_name_train=image_train_f.readline()		
img_name_train=img_name_train.strip('\n')	

while img_name_train:	
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



np.savetxt(dirTrain+'image_train_angles.txt',labels,fmt='%f')
np.savetxt(dirTrain+'image_train_angles_x.txt',labels_x,fmt='%f')
np.savetxt(dirTrain+'image_train_angles_y.txt',labels_y,fmt='%f')
np.savetxt(dirTrain+'image_train_angles_z.txt',labels_z,fmt='%f')