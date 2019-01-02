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
picNames=['045.jpg','053.jpg','107.jpg','128.jpg']
#picNames=['015.jpg','021.jpg','025.jpg','029.jpg','045.jpg','053.jpg','059.jpg','107.jpg','128.jpg']

#中心矩数
moments_num=7


min_area=15000

#将txt文件中的moments读取到矩阵f中
#矩阵F用来作中间运算
f_train=np.loadtxt(dirTrain+"image_train_features.txt",delimiter=' ')
l_train=np.loadtxt(dirTrain+'image_train_labels.txt',delimiter=' ')
F=np.empty(f_train.shape,dtype=float)
f_mean=np.mean(f_train, axis=0)
image_train_list=[]
for index,feature in enumerate(f_train):
	feature=np.abs(feature)
	s=np.sum(feature)
	if s<0.2:
		image_train_list.append(index)


flag1=0
flag2=0
image_train_f=open(dirTrain+'image_train.txt','r')
img_name_train=image_train_f.readline()		
img_name_train=img_name_train.strip('\n')	
dirF='D:\\image\\'
while flag2<len(image_train_list):
	if flag1==image_train_list[flag2]:
		img=cv2.imread(dirTrain+img_name_train)
		cv2.imwrite(dirF+img_name_train,img)
		flag2=flag2+1

	img_name_train=image_train_f.readline()		
	img_name_train=img_name_train.strip('\n')
	flag1=flag1+1
image_train_f.close()