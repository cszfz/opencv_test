#thresh test

import cv2 as cv
#读取图像，支持 bmp、jpg、png、tiff 等常用格式
img = cv.imread("000.jpg")
#创建窗口并显示图像
cv.namedWindow("Image")
cv.imshow("Image",img)
cv.waitKey(0)
rect,thresh=cv.threshold(img,50,255,0)
cv.imshow("thresh",thresh)
cv.imwrite("thresh.jpg",thresh)
cv.waitKey(0)
#释放窗口
cv2.destroyAllWindows() 
ftype py_auto_file="D:\Program Files\Sublime Text 3\sublime_text.exe" "%1"