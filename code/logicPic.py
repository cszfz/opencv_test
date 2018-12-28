#coding=utf-8

#对两张图片做逻辑运算

import cv2
dirPath="C:\\Users\\Raytine\\project\\image_thresh\\"

img1=cv2.imread(dirPath+"000.jpg")
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
img2=cv2.imread(dirPath+"001.jpg")
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

account=0
#print(sum(sum(gray1-gray2)))
xor=cv2.bitwise_xor(gray1,gray2)
cv2.imshow('xor',xor)

s=0
for i in xor:
    for j in i:
    	if j>=250:
    		s=s+1
print(s)

cv2.waitKey(0)