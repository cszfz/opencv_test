import cv2
import numpy as numpy


img=cv2.imread("result.jpg")
row,col,c=img.shape
r=col/row
print('row:'+str(row))
print('col:'+str(col))
print('r:'+str(r))
cv2.imshow('test.jpg',img)
dirPath="C:\\Users\\Raytine\\project\\image_bounding\\"
for i in range(-5,6):
	for j in range(-5,6):
		for k in range(-5,6):
			imgPath=str(i)+str(j)+str(k)+".jpg"
			img=cv2.imread(dirPath+imgPath,0)
			row,col=img.shape
			r1=col/row
			if(abs(r-r1)<0.0005):
				print(imgPath)
				cv2.imshow(imgPath,img)
				print('r1:'+str(r1))

cv2.waitKey(0)

			