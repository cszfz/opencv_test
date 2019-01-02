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
F=np.empty(f_train.shape,dtype=float)
f_mean=np.mean(f_train, axis=0)

picName='128.jpg'

#读取图片
img=cv2.imread(dirTest+picName,0)

#阈值操作
#ret,thresh = cv2.threshold(img,125,255,0)
thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
#thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

#轮廓检测,找到x光片中的检测目标
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

cnt = contours[index]
x,y,w,h = cv2.boundingRect(cnt)
x=x-4
y=y-4
w=w+8
h=h+8
result=img[y:y+h,x:x+w]

cv2.imwrite('temp1.jpg',result)

#对在x光片中找到的截图保存的检测目标进行图像分割
img=cv2.imread('temp1.jpg')
mask=np.zeros(img.shape[:2],np.uint8)
bgdModel=np.zeros((1,65),np.float64)
fgdModel=np.zeros((1,65),np.float64)
rect=(2,2,w+4,h+4)

cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

mask2=np.where((mask==2)|(mask==0),0,1).astype('uint8')
img=img*mask2[:,:,np.newaxis]

cv2.imwrite('temp2.jpg',img)


#对分割后的图像计算中心矩
img=cv2.imread('temp2.jpg',0)
cv2.imshow('test_img',img)
#阈值操作
ret,thresh = cv2.threshold(img,50,255,0)


cv2.imwrite('thresh.jpg',thresh)
#轮廓检测
_,contours,hierarchy = cv2.findContours(thresh, 1, 2)
cnt = contours[0]

#轮廓特征矩
M = cv2.moments(cnt)

#归一化中心矩
feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
print(str(feature))
#与模型库中的所有图片中心矩比较
F=f_train-feature

#求出曼哈顿距离最小的图片
F=np.abs(F)
s=np.sum(F,axis=1)
index=np.argmin(s)
m=np.min(s)

print(str(f_train[index]))

#获得测试图片的预测偏转角度	
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