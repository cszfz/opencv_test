#Shi-Tomasi all

import cv2
import numpy as np
dirPath='C:\\Users\\Raytine\\project\\image_thresh\\'
dstPath='C:\\Users\\Raytine\\project\\image_shitomasi\\'

for i in range(-5,6):
	for j in range(-5,6):
		for k in range(-5,6):
			imgPath=str(i)+str(j)+str(k)+".jpg"
			img = cv2.imread(dirPath+imgPath)
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			corners = cv2.goodFeaturesToTrack(gray,1,0.01,10)
			corners = np.int0(corners)

			for c in corners:
			    x,y = c.ravel()
			    cv2.circle(img,(x,y),3,255,-1)

			cv2.imwrite(dstPath+imgPath,img)
