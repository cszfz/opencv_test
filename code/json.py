#moments all

import cv2
import numpy as np
import json

dirPath='C:\\Users\\Raytine\\project\\image_thresh\\'
dstPath='C:\\Users\\Raytine\\project\\image_moments.txt'
filePath='C:\\Users\\Raytine\\project\\image_moments.json'

d={}
file=open(filePath,'w')


for i in range(-5,6):
	for j in range(-5,6):
		for k in range(-5,6):
			imgName=str(i)+str(j)+str(k)
			imgPath=str(i)+str(j)+str(k)+".jpg"
			img = cv2.imread(dirPath+imgPath,0)
			ret,thresh = cv2.threshold(img,50,255,0)
			_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

			cnt = contours[0]

			M = cv2.moments(cnt)

			feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
			d[imgName]=feature
			print(feature)
			#np.savetxt(dstPath,feature,fmt='%.6e')
			#print (imgPath+":[nu20:"+str(M['nu20'])+" nu11:"+str(M['nu11'])+" nu02:"+str(M['nu02'])+
				#" nu30:"+str(M['nu30'])+" nu21:"+str(M['nu21'])+" nu12:"+str(M['nu12'])+" nu03:"+str(M['nu03'])+"]")

file.write(json.dumps(d)+'\n')


