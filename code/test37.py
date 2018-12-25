#coding=utf-8
import cv2
import numpy as np
import sys
import json
import time
#图像地
dirProject='C:\\Users\\Raytine\\project\\test\\'
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

dirTests=[
		  'C:\\Users\\Raytine\\project\\test\\1\\',
		 
		  'C:\\Users\\Raytine\\project\\test\\3\\',
		  
		  'C:\\Users\\Raytine\\project\\test\\5\\',
		  
		  'C:\\Users\\Raytine\\project\\test\\7\\',
		  
		  'C:\\Users\\Raytine\\project\\test\\9\\',
		  ]
#精度要求
precisions=[0.25,0.26,0.27,0.28,0.29,0.30]

#precisions=[0.20,0.25,0.30,0.35,0.40,0.45,0.50]
#precisions=[0.10,0.11,0.12,0.13,0.14,0.15]
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



#分别记录在三个维度预测结果达到精度要求的结果
right=np.zeros([len(dirTests),len(precisions)],dtype=int)
right_x=np.zeros([len(dirTests),len(precisions)],dtype=int)
right_y=np.zeros([len(dirTests),len(precisions)],dtype=int)
right_z=np.zeros([len(dirTests),len(precisions)],dtype=int)
right_xy=np.zeros([len(dirTests),len(precisions)],dtype=int)
right_xz=np.zeros([len(dirTests),len(precisions)],dtype=int)
right_yz=np.zeros([len(dirTests),len(precisions)],dtype=int)
right_xyz=np.zeros([len(dirTests),len(precisions)],dtype=int)

#读取图像名字txt文件
image_test_f=open(dirProject+'image_test.txt','r')
img_name_test=image_test_f.readline()		
img_name_test=img_name_test.strip('\n')	

#对每一不同偏转角度的测试图片
while img_name_test:
	print(img_name_test)
	#对不同尺寸的测试图片数据集
	for ii,dirTest in enumerate(dirTests):
		#读取图片：图片文件夹+图片名字
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

		#获得测试图片的实际偏转角度
		xyz_test=(img_name_test.strip('.jpg')).split('_')
		x_test=float(xyz_test[0])
		y_test=float(xyz_test[1])
		z_test=float(xyz_test[2])

		#判断在不同精度要求小预测值是否正确
		for jj,precision in enumerate(precisions):
			x=((abs(x_test-x_train))<precision)
			y=((abs(y_test-y_train))<precision)
			z=((abs(z_test-z_train))<precision)

			if x:
				if y:
					if z:
						right_xyz[ii][jj]=right_xyz[ii][jj]+1
					else:
						right_xy[ii][jj]=right_xy[ii][jj]+1
				else:
					if z:
						right_xz[ii][jj]=right_xz[ii][jj]+1
					else:
						right_x[ii][jj]=right_x[ii][jj]+1
			else:
				if y:
					if z:
						right_yz[ii][jj]=right_yz[ii][jj]+1
					else:
						right_y[ii][jj]=right_y[ii][jj]+1
				else:
					if z:
						right_z[ii][jj]=right_z[ii][jj]+1
					else:
						right[ii][jj]=right[ii][jj]+1

	img_name_test=image_test_f.readline()	
	img_name_test=img_name_test.strip('\n')

image_test_f.close()


#将实验统计结果保存到文件中
print(right)
print(right_xyz)
np.savetxt(dirProject+(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))+'right.txt',right,fmt='%d')
np.savetxt(dirProject+(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))+'right_xyz.txt',right_xyz,fmt='%d')
