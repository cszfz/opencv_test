#coding=utf-8
import cv2
import numpy as np

img = cv2.imread('test2.jpg',0)
ret,thresh = cv2.threshold(img,50,255,0)
_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
x,y,w,h = cv2.boundingRect(cnt)

#img = cv2.rectangle(img,(x,y),(x+w,y+h),(255, 0, 0),2)
result=img[y:y+h,x:x+w]
#rect = cv2.minAreaRect(cnt)
#box = cv2.boxPoints(rect)
#box = np.int0(box)
#img = cv2.drawContours(img,[box],0,(0,0,255),2)
cv2.imshow("result",result)
cv2.imwrite("result.jpg",result)
cv2.waitKey(0)