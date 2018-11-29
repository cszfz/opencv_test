#moments test

import cv2
import numpy as np

imgPath="test2.jpg"
img = cv2.imread(imgPath,0)
ret,thresh = cv2.threshold(img,50,255,0)
_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]

M = cv2.moments(cnt)
print (imgPath+":[nu20:"+str(M['nu20'])+" nu11:"+str(M['nu11'])+" nu02:"+str(M['nu02'])+
	" nu30:"+str(M['nu30'])+" nu21:"+str(M['nu21'])+" nu12:"+str(M['nu12'])+" nu03:"+str(M['nu03'])+"]")
