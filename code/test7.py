#harris all

import cv2
import numpy as np
dirPath='C:\\Users\\Raytine\\project\\image_thresh\\'
dstPath='C:\\Users\\Raytine\\project\\image_harris\\'

for i in range(-5,6):
	for j in range(-5,6):
		for k in range(-5,6):
			imgPath=str(i)+str(j)+str(k)+".jpg"
			img = cv2.imread(dirPath+imgPath)
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

			gray = np.float32(gray)
			dst = cv2.cornerHarris(gray,2,3,0.04)

			#result is dilated for marking the corners, not important
			dst = cv2.dilate(dst,None)

			# Threshold for an optimal value, it may vary depending on the image.
			img[dst>0.01*dst.max()]=[0,0,255]

			cv2.imwrite(dstPath+imgPath,img)
