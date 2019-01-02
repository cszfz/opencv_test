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
l_train=np.loadtxt(dirTrain+"image_train_labels.txt",delimiter=' ')
F=np.empty(f_train.shape,dtype=float)
f_mean=np.mean(f_train, axis=0)




picName='053.jpg'

#读取图片
img=cv2.imread(dirTest+picName,0)

#阈值操作
#ret,thresh = cv2.threshold(img,125,255,0)
thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
#thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

#轮廓检测
_,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, 2)

l=len(contours)
f=np.empty([l,moments_num],dtype=float)

for i in range(l):
	cnt = contours[i]
	area = cv2.contourArea(cnt)
	if area>min_area:
		M = cv2.moments(cnt)
		feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
		f[i,:]=feature

f=f-f_mean
f=np.abs(f)
s=np.sum(f,axis=1)
index=np.argmin(s)

#归一化中心矩
feature=f[index]
print(str(feature))


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


result_pic_name=str(x_train)+'_'+str(y_train)+'_'+str(z_train)+'.jpg'
print('预测结果：'+result_pic_name)

flag=0
#读取图像名字txt文件
image_train_f=open(dirTrain+'image_train.txt','r')
img_name_train=image_train_f.readline()		
img_name_train=img_name_train.strip('\n')	
while flag<index:
	flag=flag+1
	img_name_train=image_train_f.readline()		
	img_name_train=img_name_train.strip('\n')
image_train_f.close()

result_img=cv2.imread(dirTrain+img_name_train)
print(img_name_train)
cv2.imshow('result',result_img)
cv2.waitKey(0)