#opencv test

import cv2

img1=cv2.imread("project\\image_thresh\\000.jpg")
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
img2=cv2.imread("project\\image_thresh\\001.jpg")
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
print(gray1)
print (sum(sum(img1-img2)))
print(sum(sum(gray1-gray2)))