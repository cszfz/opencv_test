import numpy as np
import cv2
dirPath='C:\\Users\\Raytine\\project\\image_thresh\\'
for i in range(-5,6):
	for j in range(-5,6):
		for k in range(-5,6):
			imgPath=str(i)+str(j)+str(k)+'.jpg'
			img = cv2.imread(dirPath+imgPath)
			imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			ret,thresh = cv2.threshold(imgray,127,255,0)
			image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			img = cv2.drawContours(img, contours, -1, (0,255,0), 1)
			cv2.imshow('img',img)
			cv2.waitKey()