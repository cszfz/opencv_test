#coding=utf-8
import cv2
import numpy as np
import sys
import json

#图像地址
dirTrain='C:\\Users\\Raytine\\project\\image_train\\'

#角度范围
angle=5
#角度间隔
step=0.2
#角度数目
step_number=int(angle/step*2+1)
#中心矩数
moments_num=7

#读取图像名字txt文件
image_train_f=open(dirTrain+'image_train.txt','r')
img_name_train=image_train_f.readline()     
img_name_train=img_name_train.strip('\n')   


f=np.empty([step_number*step_number*step_number,moments_num],dtype=float)

flag=0
file=open(dirTrain+'cnt.txt','w')
while flag<=100:
    flag=flag+1
    img = cv2.imread(dirTrain+img_name_train,0)
    ret,thresh = cv2.threshold(img,50,255,0)
    _,contours,hierarchy = cv2.findContours(thresh, 1, 2)
    cnt = contours[0]
    M = cv2.moments(cnt)
    print(M)
    m00=0.0
    m10=0.0
    m01=0.0
    for y,row in enumerate(thresh):
        for x,val in enumerate(row):
            m00=m00+val/255
            m10=m10+x*val/255
            m01=m01+y*val/255

    print(m00)
    print(m10)
    print(m01)

    img_name_train=image_train_f.readline()     
    img_name_train=img_name_train.strip('\n')