#coding=utf-8
import cv2
import numpy as np
import sys
import json

#图像地址
dirTrain='C:\\Users\\Raytine\\project\\image_train\\'
dirTests=['C:\\Users\\Raytine\\project\\image_test_0.009\\',
		  'C:\\Users\\Raytine\\project\\image_test_0.012\\',
		  'C:\\Users\\Raytine\\project\\image_test_0.015\\',
		  'C:\\Users\\Raytine\\project\\image_test_0.018\\',
		  'C:\\Users\\Raytine\\project\\image_test_0.021\\']



#角度范围
angle=5
#角度间隔
step=0.5
#角度数目
step_number=int(angle/step*2+1)
#中心矩数
moments_num=7

#读取图像moments的json文件
with open(dirTrain+'image_train_moments.json') as load_f:
	load_dict=json.load(load_f)


#读取图像名字txt文件
image_train_f=open(dirTrain+'image_train.txt','r')
img_name_train=image_train_f.readline()		
img_name_train=img_name_train.strip('\n')	

flag=0
f=np.empty([step_number*step_number*step_number,moments_num],dtype=float)
F=np.empty([step_number*step_number*step_number,moments_num],dtype=float)
img_train_list=[]

while img_name_train:
	img_train_list.append(img_name_train)
	f[flag,:]=load_dict[img_name_train]
	flag=flag+1
	img_name_train=image_train_f.readline()		
	img_name_train=img_name_train.strip('\n')	

image_train_f.close()

for dirTest in dirTests:
	print(dirTest)
	right=0
	right_x=0
	right_y=0
	right_z=0
	right_xy=0
	right_xz=0
	right_yz=0
	right_xyz=0

	#读取图像名字txt文件
	image_test_f=open(dirTest+'image_test.txt','r')
	img_name_test=image_test_f.readline()		
	img_name_test=img_name_test.strip('\n')	

	while img_name_test:
		img = cv2.imread(dirTest+img_name_test,0)
		ret,thresh = cv2.threshold(img,50,255,0)
		_,contours,hierarchy = cv2.findContours(thresh, 1, 2)
		cnt = contours[0]
		M = cv2.moments(cnt)
		feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
		for i in range(step_number*step_number*step_number):
			F[i,:]=f[i,:]-feature

		F=np.abs(F)
		s=np.sum(F,axis=1)
		index=np.argmin(s)
		m=np.min(s)
		img_name_train=img_train_list[index]
		xyz_train=(img_name_train.strip('.jpg')).split('_')
		x_train=float(xyz_train[0])
		y_train=float(xyz_train[1])
		z_train=float(xyz_train[2])

		xyz_test=(img_name_test.strip('.jpg')).split('_')
		x_test=float(xyz_test[0])
		y_test=float(xyz_test[1])
		z_test=float(xyz_test[2])

		x=(abs(x_test-x_train))<0.21
		y=(abs(y_test-y_train))<0.21
		z=(abs(z_test-z_train))<0.21

		if x:
			if y:
				if z:
					right_xyz=right_xyz+1
				else:
					right_xy=right_xy+1
			else:
				if z:
					right_xz=right_xz+1
				else:
					right_x=right_x+1
		else:
			if y:
				if z:
					right_yz=right_yz+1
				else:
					right_y=right_y+1
			else:
				if z:
					right_z=right_z+1
				else:
					right=right+1


		#print('test_img:'+img_name_test+'\n'+'result_img:'+img_name_train)
		img_name_test=image_test_f.readline()	
		img_name_test=img_name_test.strip('\n')

	image_test_f.close()

	print('right:'+str(right))
	print('right_x:'+str(right_x))
	print('right_y:'+str(right_y))
	print('right_z:'+str(right_z))
	print('right_xy:'+str(right_xy))
	print('right_xz:'+str(right_xz))
	print('right_yz:'+str(right_yz))
	print('right_xyz:'+str(right_xyz))