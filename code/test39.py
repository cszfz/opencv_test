#coding=utf-8
import cv2
import numpy as np
import sys
import json



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