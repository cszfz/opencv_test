#coding=utf-8
import cv2
import numpy as np
import sys
import json
import time

#图像地
dirProject='C:\\Users\\Raytine\\project\\test2\\'
dirTrain='C:\\Users\\Raytine\\project\\image_train1\\'
'''
dirTests=['C:\\Users\\Raytine\\project\\image_test0.5\\',
		  'C:\\Users\\Raytine\\project\\image_test0.6\\',
		  'C:\\Users\\Raytine\\project\\image_test0.7\\',
		  'C:\\Users\\Raytine\\project\\image_test0.8\\',
		  'C:\\Users\\Raytine\\project\\image_test0.9\\',
		  'C:\\Users\\Raytine\\project\\image_test2.0\\',
		  'C:\\Users\\Raytine\\project\\image_test2.1\\',
		  'C:\\Users\\Raytine\\project\\image_test2.2\\',
		  'C:\\Users\\Raytine\\project\\image_test2.3\\',
		  'C:\\Users\\Raytine\\project\\image_test2.4\\',
		  'C:\\Users\\Raytine\\project\\image_test2.5\\',]'''
dirTests=['C:\\Users\\Raytine\\project\\test2\\0\\',
		  'C:\\Users\\Raytine\\project\\test2\\1\\',
		  'C:\\Users\\Raytine\\project\\test2\\2\\',
		  'C:\\Users\\Raytine\\project\\test2\\3\\',
		  'C:\\Users\\Raytine\\project\\test2\\4\\',
		  'C:\\Users\\Raytine\\project\\test2\\5\\',
		  'C:\\Users\\Raytine\\project\\test2\\6\\',
		  'C:\\Users\\Raytine\\project\\test2\\7\\',
		  'C:\\Users\\Raytine\\project\\test2\\8\\',
		  'C:\\Users\\Raytine\\project\\test2\\9\\',
		  'C:\\Users\\Raytine\\project\\test2\\10\\',]

#精度要求
precisions=[0.26,0.27,0.28,0.29,0.30]

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


#将json文件中的moments读取到矩阵f中
#矩阵F用来作中间运算
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


#将实验统计结果保存到文件中
result_right_f=open('right.txt','w')
result_right_xyz_f=open('right_xyz.txt','w')


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

print(right)
print(right_xyz)
np.savetxt(dirProject+(time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime()))+'right.txt',right,fmt='%d')
np.savetxt(dirProject+(time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime()))+'right_xyz.txt',right_xyz,fmt='%d')
result_right_f.close()
result_right_xyz_f.close()