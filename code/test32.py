#moments all

import cv2
import numpy as np

dirPath='C:\\Users\\Raytine\\project\\image_thresh\\'

l=5
ll=l*2+1
flag=0
f=np.empty([ll*ll*ll,7],dtype=float)
F=np.empty([ll*ll*ll,7],dtype=float)
for i in range(-l,l+1):
	for j in range(-l,l+1):
		for k in range(-l,l+1):
			imgName=str(i)+str(j)+str(k)
			imgPath=str(i)+str(j)+str(k)+".jpg"
			img = cv2.imread(dirPath+imgPath,0)
			ret,thresh = cv2.threshold(img,50,255,0)
			_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

			cnt = contours[0]

			M = cv2.moments(cnt)
			f[flag,:]=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]
			flag=flag+1
			
print('f=')
print(f)	
print('\n')	
imgPath="test2.jpg"
img = cv2.imread(imgPath,0)
ret,thresh = cv2.threshold(img,50,255,0)
_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]

M = cv2.moments(cnt)
feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]



for i in range(ll*ll*ll):
	F[i,:]=f[i,:]-feature
print('F=')
print(F)
print('\n')	
F=np.abs(F)
print('abs(F)=')
print(F)
print('\n')	
s=np.sum(F,axis=1)
print('s=')
print(s)
print('\n')	
index=np.argmin(s)
m=np.min(s)
print('index,m=')
print(str(index)+' '+str(m))
print('\n')	
z=index%11-5
index=int((index)/11)
y=index%11-5
index=int(index/11)
x=index-5

print('filename,m=')
filename=str(x)+str(y)+str(z)+'.jpg'
print(filename+' '+str(m))
print('\n')	

img=cv2.imread(dirPath+filename)
cv2.imshow(filename,img)
cv2.waitKey(0)