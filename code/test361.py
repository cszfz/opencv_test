#coding=utf-8
#保存测试数据的moments特征以及对应angle标签

import cv2
import numpy as np
import sys

dirTest='C:\\Users\\Raytine\\project\\test1\\'

#测试集数目
tests_num=5
#单个测试集图片数
test_num=2000
#中心矩数
moments_num=7

angle_num=3

#读取图像名字txt文件
image_test_f=open(dirTest+'image_test.txt','r')
img_name_test=image_test_f.readline()		
img_name_test=img_name_test.strip('\n')	


f=np.empty([tests_num,test_num,moments_num],dtype=float)

flag=0

labels=np.empty([test_num,angle_num],dtype=float)
labels_x=np.empty([test_num,1],dtype=float)
labels_y=np.empty([test_num,1],dtype=float)
labels_z=np.empty([test_num,1],dtype=float)

#对每一不同偏转角度的测试图片
while img_name_test:
	print(img_name_test)
	#对不同尺寸的测试图片数据集
	for ii in range(tests_num):
		#读取图片：图片文件夹+图片名字
		img = cv2.imread(dirTest+str(ii)+'\\'+img_name_test,0)

		#阈值操作
		ret,thresh = cv2.threshold(img,50,255,0)

		#轮廓检测
		_,contours,hierarchy = cv2.findContours(thresh, 1, 2)
		cnt = contours[0]

		#轮廓特征矩
		M = cv2.moments(cnt)

		#归一化中心矩
		f[ii,flag,:]=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]


	xyz_test=(img_name_test.strip('.jpg')).split('_')
	x_test=float(xyz_test[0])
	y_test=float(xyz_test[1])
	z_test=float(xyz_test[2])
	labels[flag]=[x_test,y_test,z_test]
	labels_x[flag]=x_test
	labels_y[flag]=y_test
	labels_z[flag]=z_test

	img_name_test=image_test_f.readline()	
	img_name_test=img_name_test.strip('\n')
	flag=flag+1

image_test_f.close()

np.savetxt(dirTest+'image_test_labels.txt',labels,fmt='%f')
np.savetxt(dirTest+'image_test_labels_x.txt',labels_x,fmt='%f')
np.savetxt(dirTest+'image_test_labels_y.txt',labels_y,fmt='%f')
np.savetxt(dirTest+'image_test_labels_z.txt',labels_z,fmt='%f')

for ii in range(tests_num):
	np.savetxt(dirTest+str(ii)+'.txt',f[ii],fmt='%f')


