# coding=utf-8
import cv2
import numpy as np
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

scale=0.015
WIDTH=600
HEIGHT=600

trains = [['15l', '2l', '25l', '3l', '4l'],
          ['15r', '2r', '25r', '3r', '4r']]
results = [[[['外旋',' 外翻'],['外旋',' 内翻']],
            [['内旋',' 外翻'],['内旋',' 内翻']]],
           [[['内旋',' 内翻'],['内旋',' 外翻']],
            [['外旋',' 内翻'],['外旋',' 外翻']]]]




class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(542, 342)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(40, 60, 471, 31))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_6.setGeometry(QtCore.QRect(240, 10, 30, 16))
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_7 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_7.setGeometry(QtCore.QRect(290, 10, 30, 16))
        self.radioButton_7.setObjectName("radioButton_7")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 54, 12))
        self.label_2.setObjectName("label_2")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_4.setGeometry(QtCore.QRect(130, 10, 30, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_5.setGeometry(QtCore.QRect(180, 10, 43, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(70, 10, 43, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(40, 9, 471, 31))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton.setGeometry(QtCore.QRect(70, 10, 89, 16))
        self.radioButton.setObjectName("radioButton")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 54, 12))
        self.label.setObjectName("label")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_2.setGeometry(QtCore.QRect(130, 10, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(40, 110, 471, 61))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 20, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(310, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit.setGeometry(QtCore.QRect(70, 20, 231, 20))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.label_3.setObjectName("label_3")
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(40, 190, 471, 141))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QtCore.QRect(70, 10, 231, 81))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 54, 20))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "人工膝关节预测"))
        self.radioButton_6.setText(_translate("Dialog", "3"))
        self.radioButton_7.setText(_translate("Dialog", "4"))
        self.label_2.setText(_translate("Dialog", "关节型号："))
        self.radioButton_4.setText(_translate("Dialog", "2"))
        self.radioButton_5.setText(_translate("Dialog", "2.5"))
        self.radioButton_3.setText(_translate("Dialog", "1.5"))
        self.radioButton.setText(_translate("Dialog", "左边"))
        self.label.setText(_translate("Dialog", "关节位置："))
        self.radioButton_2.setText(_translate("Dialog", "右边"))
        self.pushButton_2.setText(_translate("Dialog", "确定"))
        self.pushButton.setText(_translate("Dialog", "选择图片"))
        self.label_3.setText(_translate("Dialog", "测试图片："))
        self.label_4.setText(_translate("Dialog", "预测结果："))

    def enable(self):

        # 定义位置表示
        self.location = 0
        self.radioButton.setChecked(True)

        # 定义型号表示
        self.size = 0
        self.radioButton_3.setChecked(True)

        # 定义路径
        self.cwd = os.getcwd()

        # 设置信号
        self.pushButton.clicked.connect(self.btn_select_pic)
        self.pushButton_2.clicked.connect(self.btn_predict)

        self.result_x=0.0
        self.result_y=0.0
        self.result_z=0.0
        self.y_sign=0
        self.z_sign=0



    def btn_select_pic(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self, "选取图片", self.cwd, "jpg Files (*.jpg)")

        if fileName_choose == "":
            # print("\n取消选择")
            return

        else:
            self.pushButton_2.setEnabled(True)
            self.lineEdit.setText(fileName_choose)

        # print("\n你选择的图片为:")
        # print(fileName_choose)

    def btn_predict(self):

        fileName_choose = self.lineEdit.text()

        if self.radioButton.isChecked():
            self.location = 0
        if self.radioButton_2.isChecked():
            self.location = 1

        if self.radioButton_3.isChecked():
            self.size = 0
        if self.radioButton_4.isChecked():
            self.size = 1
        if self.radioButton_5.isChecked():
            self.size = 2
        if self.radioButton_6.isChecked():
            self.size = 3
        if self.radioButton_7.isChecked():
            self.size = 4

        dirTrain = 'DependentFiles\\txt\\' + trains[self.location][self.size] + '\\'

        # 中心矩数
        moments_num = 7
        min_area = 15000
        f_mean = np.loadtxt(dirTrain + "image_train_mean.txt", delimiter=' ')

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
        # print(str(feature))

        # 将txt文件中的moments读取到矩阵f中
        # 矩阵F用来作中间运算
        f_train = np.loadtxt(dirTrain + "image_train_features.txt", delimiter=' ')
        l_train = np.loadtxt(dirTrain + "image_train_labels.txt", delimiter=' ')
        F = np.empty(f_train.shape, dtype=float)

        # 与模型库中的所有图片中心矩比较l
        F = f_train - feature
        # 求出曼哈顿距离最小的图片
        F = np.abs(F)
        s = np.sum(F, axis=1)
        index = np.argmin(s)


        self.result_x=l_train[index][0]
        self.result_y=l_train[index][1]
        self.result_z=l_train[index][2]



        if self.result_y<0:
            self.y_sign=1
        if self.result_z<0:
            self.z_sign=1

        result=results[self.location][self.y_sign][self.z_sign]
        result_str=result[0]+str(abs(self.result_y))+','+result[1]+str(abs(self.result_z))






        self.textEdit.setText(result_str)


        show_result()

def show_result():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("result")
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
    glutDisplayFunc(display)
    glutMainLoop()
    return



class MainForm(QWidget, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi((self))
        self.enable()


def display():
    model_file = 'DependentFiles\\model\\'+trains[mainForm.size][mainForm.location] + '.off'
    glClearColor(0.0,0.0,0.0,0.0)
    glClearDepth(2.0)
    glShadeModel(GL_SMOOTH)

    showFacelist = glGenLists(1)
    mf=open(model_file,'r')
    mf.readline()
    line=mf.readline()
    num=line.split(' ')
    vertex_num=int(num[0])
    face_num=int(num[1])

    points=np.empty([vertex_num,3],dtype=float)

    for i in range(vertex_num):
        line=mf.readline()
        vertex=line.split(' ')
        points[i][0]=float(vertex[0])
        points[i][1]=float(vertex[1])
        points[i][2]=float(vertex[2])


    glNewList(showFacelist, GL_COMPILE)

    for i in range(face_num):
        line=mf.readline()
        vertexs=line.split(' ')

        glBegin(GL_TRIANGLES)
        glVertex3fv(points[int(vertexs[1])])
        glVertex3fv(points[int(vertexs[2])])
        glVertex3fv(points[int(vertexs[3])])
        glEnd()

    glEndList()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(mainForm.result_x,1.0,0.0,0.0)
    glRotatef(mainForm.result_y,0.0,1.0,0.0)
    glRotatef(mainForm.result_z,0.0,0.0,1.0)

    glTranslatef(0.0,-0.35,0.0)

    glScalef(scale,scale,scale)

    glCallList(showFacelist)

    glutSwapBuffers()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainForm = MainForm() 
    mainForm.show()
    sys.exit(app.exec_())