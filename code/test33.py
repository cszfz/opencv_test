#moments all

import cv2
import numpy as np

dirPath='C:\\Users\\Raytine\\project\\image_thresh\\'
dirTest='C:\\Users\\Raytine\\project\\image_test\\'


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
			#print(imgPath+':'+str(f[flag,:]))
			flag=flag+1
			
for ii in np.arange(0,2,0.2):
	for jj in np.arange(0,2,0.2):
		for kk in np.arange(0,2,0.2):
			imgName=str('%.1f'%ii)+'_'+str('%.1f'%jj)+'_'+str('%.1f'%kk)
			imgPath=imgName+'.jpg'
			print(imgPath)
			img = cv2.imread(dirTest+imgPath,0)
			#cv2.imshow(imgPath,img)
			ret,thresh = cv2.threshold(img,50,255,0)
			_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

			cnt = contours[0]

			M = cv2.moments(cnt)
			feature=[M['nu20'],M['nu11'],M['nu02'],M['nu30'],M['nu21'],M['nu12'],M['nu03']]



			for i in range(ll*ll*ll):
				F[i,:]=f[i,:]-feature

			F=np.abs(F)

			s=np.sum(F,axis=1)
				
			index=np.argmin(s)
			m=np.min(s)

			z=index%11-5
			index=int((index)/11)
			y=index%11-5
			index=int(index/11)
			x=index-5




			filename=str(x)+str(y)+str(z)+'.jpg'


			img=cv2.imread(dirPath+filename)
			#cv2.imshow(filename,img)
			#cv2.waitKey(0)
			print('test_img:('+str(int(round(ii)))+str(int(round(jj)))+str(int(round(kk)))+')'+imgPath+'   '+'result'+filename)