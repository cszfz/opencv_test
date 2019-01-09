

#coding=utf-8
import cv2
import numpy as np
import sys

import time

#图像地址
dirTrains=[
		   'D:\\image\\train2lt\\',
		   ]

dirTest='D:\\image\\'
picNamesR=['045.jpg','054.jpg','107.jpg','128.jpg']
picNamesL=['644.jpg','648.jpg','657.jpg','701.jpg','705.jpg','708.jpg']
#中心矩数
moments_num=7

min_area=15000


#f_mean=np.mean(f_train, axis=0)
f_mean=np.loadtxt(dirTrains[0]+"image_train_mean.txt",delimiter=' ')
picName='00000003.TIF'

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
x=x-3
y=y-3
w=w+6
h=h+6
result=img[y:y+h,x:x+w]

cv2.imwrite('temp1.jpg',result)

#对在x光片中找到的截图保存的检测目标进行图像分割
img=cv2.imread('temp1.jpg')
cv2.imshow('test_img',img)
mask=np.zeros(img.shape[:2],np.uint8)
bgdModel=np.zeros((1,65),np.float64)
fgdModel=np.zeros((1,65),np.float64)
rect=(3,3,w-6,h-6)

cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
print(cv2.GC_PR_FGD)
mask2=np.where((mask==2)|(mask==0),0,1).astype('uint8')
img=img*mask2[:,:,np.newaxis]

cv2.imwrite('temp2.jpg',img)


#对分割后的图像计算中心矩
img=cv2.imread('temp2.jpg',0)

#阈值操作
ret,thresh = cv2.threshold(img,50,255,0)


cv2.imwrite('thresh.jpg',thresh)
