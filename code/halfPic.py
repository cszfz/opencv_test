#coding=utf-8
import cv2
import copy
picDir='D:\\image\\lt\\'
picName='649.jpg'
img=cv2.imread(picDir+picName)


shape = img.shape
print(shape)
dst=img[0:shape[0],int(shape[1]/2):shape[1]]
cv2.imshow('flip',dst)
cv2.imwrite(picDir+'648.jpg',dst)