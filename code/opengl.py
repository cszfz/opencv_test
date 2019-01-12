from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
import numpy as np
import sys

scale=0.02
WIDTH=900
HEIGHT=900
xr=0.0
yr=0.0
zr=0.0
model_file='D:\\image\\model\\2lt.off'




def display():
	glClearColor(0.0,0.0,0.0,0.0)
	glClearDepth(2.0)
	glShadeModel(GL_SMOOTH)

	showFacelist = glGenLists(1)
	mf=open(model_file,'r')
	line=mf.readline()
	line=mf.readline()
	num=line.split(' ')
	vertex_num=int(num[0])
	face_num=int(num[1])

	points=np.empty([vertex_num,3],dtype=float)

	print(vertex_num,face_num)

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

	glRotatef(xr,1.0,0.0,0.0)
	glRotatef(yr,0.0,1.0,0.0)
	glRotatef(zr,0.0,0.0,1.0)

	glTranslatef(0.0,-0.35,0.0)

	glScalef(scale,scale,scale)

	glCallList(showFacelist)

	glutSwapBuffers()

if __name__ == "__main__":
	glutInit()
	glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(WIDTH, HEIGHT)
	glutCreateWindow("Mesh Viewer")
	glutDisplayFunc(display)

	glutMainLoop()


