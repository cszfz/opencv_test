
#moments all

import cv2
import numpy as np
import json

dirPath='C:\\Users\\Raytine\\project\\image_thresh\\'
dstPath='C:\\Users\\Raytine\\project\\image_moments.txt'
filePath='C:\\Users\\Raytine\\project\\image_moments.json'

with open(filePath) as f:
	d=json.load(f)

f1=np.empty([1,7],dtype=float)
f2=np.empty([1,7],dtype=float)
imgPath="test2.jpg"
img = cv2.imread(imgPath,0)
ret,thresh = cv2.threshold(img,50,255,0)
_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]

M = cv2.moments(cnt)
f1[0,:]=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]


imgPath="110.jpg"
img = cv2.imread(dirPath+imgPath,0)
ret,thresh = cv2.threshold(img,50,255,0)
_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]

M = cv2.moments(cnt)
f2[0,:]=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]

print(np.sum(np.abs(f1[0,:]-f2[0,:])))