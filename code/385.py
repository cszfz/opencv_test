#coding=utf-8
#保存训练数据的moments特征以及对应angle标签
import cv2
import numpy as np
import sys


#图像地址
dirTrains=[
		   'D:\\image\\train4\\']


step_number_x=61
step_number_y=101
step_number_z=21
#中心矩数
moments_num=7

angle_num=3


labels=np.empty([step_number_x*step_number_y*step_number_z,angle_num],dtype=float)
labels_x=np.empty([step_number_x*step_number_y*step_number_z,1],dtype=float)
labels_y=np.empty([step_number_x*step_number_y*step_number_z,1],dtype=float)
labels_z=np.empty([step_number_x*step_number_y*step_number_z,1],dtype=float)

features=np.empty([step_number_x*step_number_y*step_number_z,moments_num],dtype=float)

for dirTrain in dirTrains:

	flag=0
	#读取图像名字txt文件
	image_train_f=open(dirTrain+'image_train.txt','r')
	img_name_train=image_train_f.readline()		
	img_name_train=img_name_train.strip('\n')	
	image_train_list=open(dirTrain+'image_train_list.txt','w')

	while img_name_train:

		print(flag)

		img = cv2.imread(dirTrain+img_name_train,0)
		ret,thresh = cv2.threshold(img,50,255,0)
		#thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
		_,contours,hierarchy = cv2.findContours(thresh, 1, 2)
		cnt = contours[0]
		M = cv2.moments(cnt)
		features[flag]=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]

		if np.sum(np.abs(features[flag]))>0.2:

			image_train_list.write(img_name_train+'\n')

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

	f_mean=np.mean(features, axis=0)

	image_train_f.close()
	image_train_list.close()


	featuress=np.empty([flag,moments_num],dtype=float)
	labelss=np.empty([flag,angle_num],dtype=float)
	labelss_x=np.empty([flag,1],dtype=float)
	labelss_y=np.empty([flag,1],dtype=float)
	labelss_z=np.empty([flag,1],dtype=float)


	for i in range(flag):
		featuress[i]=features[i]
		labelss[i]=labels[i]
		labelss_x[i]=labels_x[i]
		labelss_y[i]=labels_y[i]
		labelss_z[i]=labels_z[i]

	np.savetxt(dirTrain+'image_train_features.txt',featuress,fmt='%f')
	np.savetxt(dirTrain+'image_train_labels.txt',labelss,fmt='%f')
	np.savetxt(dirTrain+'image_train_labels_x.txt',labelss_x,fmt='%f')
	np.savetxt(dirTrain+'image_train_labels_y.txt',labelss_y,fmt='%f')
	np.savetxt(dirTrain+'image_train_labels_z.txt',labelss_z,fmt='%f')
	np.savetxt(dirTrain+'image_train_mean.txt',f_mean,fmt='%f')