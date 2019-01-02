#coding=utf-8
import cv2
import numpy as np
import sys
import time
#图像地
dirTest='C:\\Users\\Raytine\\project\\test3\\'
dirTrain='C:\\Users\\Raytine\\project\\image_train\\'
#精度要求
precisions=[0.10,0.14,0.18,0.22,0.26,0.30]
#precisions=[0.25,0.26,0.27,0.28,0.29,0.30]
#precisions=[0.20,0.25,0.30,0.35,0.40,0.45,0.50]
#precisions=[0.10,0.11,0.12,0.13,0.14,0.15]
#角度范围
angle_x=10
angle_y=10
angle_z=5
#角度间隔
step=0.2
#角度数目
step_number_x=int(angle_x/step*2+1)
step_number_y=int(angle_y/step*2+1)
step_number_z=int(angle_z/step*2+1)
#中心矩数
moments_num=7

#测试集数目
tests_num=5
#单个测试集图片数
test_num=2000

#将txt文件中的moments特征读取到矩阵中
f_train=np.loadtxt(dirTrain+"image_train_features.txt",delimiter=' ')

#txt文件中的angles标签读取到矩阵中
l_train=np.loadtxt(dirTrain+'image_train_labels.txt',delimiter=' ')
l_test=np.loadtxt(dirTest+'image_test_labels.txt',delimiter=' ')
#矩阵F用来作中间运算
F=np.empty([step_number_x*step_number_y*step_number_z,moments_num],dtype=float)



#分别记录在三个维度预测结果达到精度要求的结果
right=np.zeros([tests_num,len(precisions)],dtype=int)
right_x=np.zeros([tests_num,len(precisions)],dtype=int)
right_y=np.zeros([tests_num,len(precisions)],dtype=int)
right_z=np.zeros([tests_num,len(precisions)],dtype=int)
right_xy=np.zeros([tests_num,len(precisions)],dtype=int)
right_xz=np.zeros([tests_num,len(precisions)],dtype=int)
right_yz=np.zeros([tests_num,len(precisions)],dtype=int)
right_xyz=np.zeros([tests_num,len(precisions)],dtype=int)


#对不同尺寸的测试图片数据集
for ii in range(tests_num):

	f_test=np.loadtxt(dirTest+str(ii)+'.txt',delimiter=' ')

	#对每一不同偏转角度的测试图片
	for jj,xyz_test in enumerate(l_test) :

		print('epoch:'+str(ii)+'-'+str(jj))

		#与模型库中的所有图片中心矩比较
		F=f_train-f_test[jj]

		#求出曼哈顿距离最小的图片
		F=np.abs(F)
		s=np.sum(F,axis=1)
		index=np.argmin(s)
		m=np.min(s)

		#获得测试图片的预测偏转角度
		
		xyz_train=l_train[index]
		x_train=float(xyz_train[0])
		y_train=float(xyz_train[1])
		z_train=float(xyz_train[2])

		x_test=float(xyz_test[0])
		y_test=float(xyz_test[1])
		z_test=float(xyz_test[2])

		#判断在不同精度要求小预测值是否正确
		for kk,precision in enumerate(precisions):
			x=((abs(x_test-x_train))<precision)
			y=((abs(y_test-y_train))<precision)
			z=((abs(z_test-z_train))<precision)

			if x:
				if y:
					if z:
						right_xyz[ii][kk]=right_xyz[ii][kk]+1
					else:
						right_xy[ii][kk]=right_xy[ii][kk]+1
				else:
					if z:
						right_xz[ii][kk]=right_xz[ii][kk]+1
					else:
						right_x[ii][kk]=right_x[ii][kk]+1
			else:
				if y:
					if z:
						right_yz[ii][kk]=right_yz[ii][kk]+1
					else:
						right_y[ii][kk]=right_y[ii][kk]+1
				else:
					if z:
						right_z[ii][kk]=right_z[ii][kk]+1
					else:
						right[ii][kk]=right[ii][kk]+1

#将实验统计结果保存到文件中
print(right)
print(right_xyz)
np.savetxt(dirTest+(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))+'right.txt',right,fmt='%d')
np.savetxt(dirTest+(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))+'right_xyz.txt',right_xyz,fmt='%d')
