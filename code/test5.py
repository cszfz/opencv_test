#thresh all
import cv2 as cv
dirPath='C:\\Users\\Raytine\\project\\image\\'
dstPath='C:\\Users\\Raytine\\project\\image_thresh\\'

for i in range(-5,6):
	for j in range(-5,6):
		for k in range(-5,6):
			imgPath=str(i)+str(j)+str(k)+".jpg"
			img = cv.imread(dirPath+imgPath)
			

			rect,thresh=cv.threshold(img,50,255,0)
			cv.imwrite(dstPath+imgPath,thresh)


