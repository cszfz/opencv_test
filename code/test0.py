import cv2
import numpy as numpy

dirPath="C:\\Users\\Raytine\\project\\image_thresh\\"
dstPath="C:\\Users\\Raytine\\project\\image_bounding\\"
for i in range(-5,6):
	for j in range(-5,6):
		for k in range(-5,6):
			imgPath=str(i)+str(j)+str(k)+".jpg"
			img=cv2.imread(dirPath+imgPath,0)
			ret,thresh = cv2.threshold(img,50,255,0)
			_,contours,hierarchy = cv2.findContours(thresh, 1, 2)
			cnt = contours[0]
			x,y,w,h = cv2.boundingRect(cnt)
			result=img[y:y+h,x:x+w]
			cv2.imwrite(dstPath+imgPath,result)
			