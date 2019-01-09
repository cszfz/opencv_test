# coding=utf-8
import cv2
import numpy as np
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(536, 279)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 30, 54, 12))
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(110, 30, 89, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(170, 30, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 80, 54, 12))
        self.label_2.setObjectName("label_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_3.setGeometry(QtCore.QRect(110, 80, 89, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_4.setGeometry(QtCore.QRect(160, 80, 89, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_5.setGeometry(QtCore.QRect(200, 80, 89, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_6.setGeometry(QtCore.QRect(250, 80, 89, 16))
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_7 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_7.setGeometry(QtCore.QRect(300, 80, 89, 16))
        self.radioButton_7.setObjectName("radioButton_7")
        self.radioButton_8 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_8.setGeometry(QtCore.QRect(340, 80, 89, 16))
        self.radioButton_8.setObjectName("radioButton_8")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(310, 110, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(110, 110, 181, 21))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 110, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(120, 170, 251, 71))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 120, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(50, 170, 54, 12))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)

        # 设置信号
        self.pushButton.clicked.connect(self.slot_btn_chooseFile)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "关节位置："))
        self.radioButton.setText(_translate("Dialog", "左边"))
        self.radioButton_2.setText(_translate("Dialog", "右边"))
        self.label_2.setText(_translate("Dialog", "关节型号："))
        self.radioButton_3.setText(_translate("Dialog", "1.5"))
        self.radioButton_4.setText(_translate("Dialog", "2"))
        self.radioButton_5.setText(_translate("Dialog", "2.5"))
        self.radioButton_6.setText(_translate("Dialog", "3"))
        self.radioButton_7.setText(_translate("Dialog", "4"))
        self.radioButton_8.setText(_translate("Dialog", "未知"))
        self.pushButton.setText(_translate("Dialog", "选择图片"))

        self.pushButton_2.setText(_translate("Dialog", "确定"))
        self.label_3.setText(_translate("Dialog", "测试图片："))
        self.label_4.setText(_translate("Dialog", "预测结果："))

    def slot_btn_chooseFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self, "选取图片", self.cwd, "jpg Files (*.jpg)")

        if fileName_choose == "":
            print("\n取消选择")
            return

        print("\n你选择的图片为:")
        print(fileName_choose)


        dirTrains = ['D:\\image\\train2lt\\']

        # 中心矩数
        moments_num = 7
        min_area = 15000
        f_mean = np.loadtxt(dirTrains[0] + "image_train_mean.txt", delimiter=' ')

        # 读取图片
        img = cv2.imread(fileName_choose, 0)
        # 阈值操作
        thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # 轮廓检测,找到x光片中的检测目标
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, 2)
        l = len(contours)
        f = np.empty([l, moments_num], dtype=float)

        for i in range(l):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if area > min_area:
                M = cv2.moments(cnt)
                feature = [M['nu20'], M['nu11'], M['nu02'], M['nu30'], M['nu21'], M['nu12'], M['nu03']]
                f[i, :] = feature

        f = f - f_mean
        f = np.abs(f)
        s = np.sum(f, axis=1)
        index = np.argmin(s)

        cnt = contours[index]
        x, y, w, h = cv2.boundingRect(cnt)
        x = x - 6
        y = y - 6
        w = w + 12
        h = h + 12
        target = img[y:y + h, x:x + w]

        cv2.imwrite('target.jpg', target)
        # 对在x光片中找到的截图保存的检测目标进行图像分割
        img = cv2.imread('target.jpg')
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (3, 3, w - 6, h - 6)

        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]

        cv2.imwrite('segmentation.jpg', img)
        # 对分割后的图像计算中心矩
        img = cv2.imread('segmentation.jpg', 0)

        # 阈值操作
        ret, thresh = cv2.threshold(img, 50, 255, 0)
        cv2.imwrite('thresh.jpg', thresh)

        # 轮廓检测
        _, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]

        # 轮廓特征矩
        M = cv2.moments(cnt)

        # 归一化中心矩
        feature = [M['nu20'], M['nu11'], M['nu02'], M['nu30'], M['nu21'], M['nu12'], M['nu03']]
        print(str(feature))
        for dirTrain in dirTrains:
            # 将txt文件中的moments读取到矩阵f中
            # 矩阵F用来作中间运算
            f_train = np.loadtxt(dirTrain + "image_train_features.txt", delimiter=' ')
            F = np.empty(f_train.shape, dtype=float)

            # 与模型库中的所有图片中心矩比较l
            F = f_train - feature
            # 求出曼哈顿距离最小的图片
            F = np.abs(F)
            s = np.sum(F, axis=1)
            index = np.argmin(s)

            # 获得测试图片的预测偏转角度
            flag = 0
            # 读取图像名字txt文件
            image_train_f = open(dirTrain + 'image_train_list.txt', 'r')
            img_name_train = image_train_f.readline()
            img_name_train = img_name_train.strip('\n')
            while flag < index:
                flag = flag + 1
                img_name_train = image_train_f.readline()
                img_name_train = img_name_train.strip('\n')
            image_train_f.close()

            print(str(f_train[index]))
            result_img = cv2.imread(dirTrain + img_name_train)
            cv2.imwrite('result.jpg', result_img)
            print('测试结果:'+img_name_train)

class MainForm(QWidget,Ui_Dialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi((self))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec_())