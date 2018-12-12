#coding=utf-8
import cv2
import numpy as np
import sys
import json


dirProject='C:\\Users\\Raytine\\project\\test1\\'
f=np.empty([3,2],dtype=float)
F=np.empty([3,2],dtype=float)



f[0,:]=[1,2]
f[1,:]=[3,4]
f[2,:]=[5,6]
feature=[2.5, 2.5]

for i in range(3):
	F[i,:]=f[i,:]-feature

F=np.power(F,2)

print(F)
s=np.sum(F,axis=1)
print(s)
index=np.argmin(s)
print(index)
m=np.min(s)
print(m)

hhh=[[12,0,0,0,0,0,0],
 [13,1,1,1,1,1,1],
 [15,1,1,1,1,1,1],
 [15,0,0,0,0,0,0],
 [13,1,1,1,1,1,1],
 [14,2,2,2,2,2,2],
 [14,3,3,3,3,3,3],
 [18,6,6,5,5,4,4],
 [14,2,2,2,2,2,2],
 [13,3,2,2,2,2,2],
 [15,4,3,3,3,3,3]]
np.savetxt(dirProject+'result.txt',hhh,fmt='%d')

print(time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime())) 