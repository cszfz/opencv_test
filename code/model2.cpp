#include <iostream>  
#include <OpenMesh/Core/IO/MeshIO.hh>  
#include <OpenMesh/Core/Mesh/TriMesh_ArrayKernelT.hh>  
#include "GL\glut.h"
#include <math.h>
#include <Windows.h>
#include <string>
#include <sstream>

#include<stdio.h>
#include<FreeImage.h> 

//#pragma comment(lib,"FreeImage.lib")

using namespace std;
typedef OpenMesh::TriMesh_ArrayKernelT<> MyMesh;
//模型地址
const string file_1 = "D:\\image\\model\\15rt.off";

//图片存放地址
const char *dirTrain="D:\\image\\train15rt\\";

const char *image_txt="D:\\image\\train15rt\\image_train.txt";

//设置角度范围
int angle_x=30;
int angle_y=60;
int angle_z=20;

//起始角度
int s_x=-10;
int s_y=-30;
int s_z=-10;

//设置步长
float step =5;

//迭代次数
int range_x=angle_x*10/step;
int range_y=angle_y*10/step;
int range_z=angle_z*10/step;


//起始迭代
int minus_range_x=s_x*10;
int minus_range_y=s_y*10;
int minus_range_z=s_z*10;


//与实现角度大小相关的参数，
int xNum=minus_range_x;
int yNum=minus_range_y;
int zNum=minus_range_z;

float xRotate;
float yRotate;
float zRotate;

//float scale = 0.0145;
float scale=0.02;


//文件读取有关的
MyMesh mesh;


int flag=1;

GLuint showFaceList, showWireList;
int showstate = 1;
bool showFace = true;
bool showWire = false;
bool showFlatlines = false;

int WIDTH=900,HEIGHT=900;
FIBITMAP* bitmap = FreeImage_Allocate(WIDTH, HEIGHT, 24, 8, 8, 8);
unsigned char *mpixels = new unsigned char[WIDTH * HEIGHT * 3];

int first=0;
void grab(char *pName)
{
    glReadBuffer(GL_FRONT);
    glReadPixels(0, 0, WIDTH, HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, mpixels);
    glReadBuffer(GL_BACK);
    for(int i = 0; i < (int)WIDTH*HEIGHT*3; i += 3)
    {   
        mpixels[i] ^= mpixels[i+2] ^= mpixels[i] ^= mpixels[i+2];
    }
    for(int y = 0 ; y < FreeImage_GetHeight(bitmap); y++)
    {
        BYTE *bits = FreeImage_GetScanLine(bitmap, y);
        for(int x = 0 ; x < FreeImage_GetWidth(bitmap); x++)
        {
            bits[0] = mpixels[(y*WIDTH+x) * 3 + 0];
            bits[1] = mpixels[(y*WIDTH+x) * 3 + 1];
            bits[2] = mpixels[(y*WIDTH+x) * 3 + 2];
            bits += 3;
        }
    }

    FreeImage_Save(FIF_JPEG, bitmap, pName, JPEG_DEFAULT);

}
//³õÊ¼»¯¶¥µãºÍÃæ   
void initGL()
{
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glClearDepth(2.0);
    glShadeModel(GL_SMOOTH);
   
    showFaceList = glGenLists(1);
    showWireList = glGenLists(1);
    int temp = mesh.n_edges();

    // »æÖÆ wire 
    glNewList(showWireList, GL_COMPILE);
  
    glLineWidth(1.0f);
    glColor3f(1.0f, 1.0f, 1.0f);
    glBegin(GL_LINES);
    for (MyMesh::HalfedgeIter he_it = mesh.halfedges_begin(); he_it != mesh.halfedges_end(); ++he_it) {
        //Á´½ÓÕâ¸öÓÐÏò±ßµÄÆðµãºÍÖÕµã
        glVertex3fv(mesh.point(mesh.from_vertex_handle(*he_it)).data());
        //cout<<mesh.point(mesh.from_vertex_handle(*he_it)).data()<<endl;
        glVertex3fv(mesh.point(mesh.to_vertex_handle(*he_it)).data());
    }
    glEnd();
    glEndList();

    // »æÖÆflat
    glNewList(showFaceList, GL_COMPILE);
    for (MyMesh::FaceIter f_it = mesh.faces_begin(); f_it != mesh.faces_end(); ++f_it) {
        glBegin(GL_TRIANGLES);
        for (MyMesh::FaceVertexIter fv_it = mesh.fv_iter(*f_it); fv_it.is_valid(); ++fv_it) {
            glNormal3fv(mesh.normal(*fv_it).data());
            glVertex3fv(mesh.point(*fv_it).data());
        }
        glEnd();
    }
    glEndList();
}


void createName(float x, float y, float z,char* n)
{
    
    int i=0;
    char*xx=new char[20];
    sprintf(xx, "%g", x);
    for(int j=0;j<strlen(xx);j++)
    {
        n[i++]=xx[j];
    }
    n[i++]='_';
    char*yy=new char[20];
    sprintf(yy, "%g", y);
    for(int j=0;j<strlen(yy);j++)
    {
        n[i++]=yy[j];
    }
 
    n[i++]='_';
    char*zz=new char[20];
    sprintf(zz, "%g", z);
    for(int j=0;j<strlen(zz);j++)
    {
        n[i++]=zz[j];
    }
    
    n[i++]='.';
    n[i++]='j';
    n[i++]='p';
    n[i++]='g';
    n[i++]='\0';

}

void createFileName(char* pName,char*fName)
{
	int i=0;
	for(int j=0;j<strlen(dirTrain);j++)
    {
        fName[i++]=dirTrain[j];
    }
	fName[i++]='\\';
	for(int j=0;j<strlen(pName);j++)
	{
		fName[i++]=pName[j];
	}
	fName[i++]='\0';
}



// ¶ÁÈ¡ÎÄ¼þµÄº¯Êý
void readfile(string file) {
    // ÇëÇó¶¥µã·¨Ïß vertex normals
    mesh.request_vertex_normals();
    //Èç¹û²»´æÔÚ¶¥µã·¨Ïß£¬Ôò±¨´í 
    if (!mesh.has_vertex_normals())
    {
        cout << "´íÎó£º±ê×¼¶¨µãÊôÐÔ ¡°·¨Ïß¡±²»´æÔÚ" << endl;
        return;
    }
    // Èç¹ûÓÐ¶¥µã·¢ÏÖÔò¶ÁÈ¡ÎÄ¼þ 
    OpenMesh::IO::Options opt;
    if (!OpenMesh::IO::read_mesh(mesh, file, opt))
    {
        cout << "ÎÞ·¨¶ÁÈ¡ÎÄ¼þ:" << file << endl;
        return;
    }
    else cout << "³É¹¦¶ÁÈ¡ÎÄ¼þ:" << file << endl;
    cout << endl; 

    if (!opt.check(OpenMesh::IO::Options::VertexNormal))
    {
        // Í¨¹ýÃæ·¨Ïß¼ÆËã¶¥µã·¨Ïß
        mesh.request_face_normals();
        // mesh¼ÆËã³ö¶¥µã·¨Ïß
        mesh.update_normals();
        // ÊÍ·ÅÃæ·¨Ïß
        mesh.release_face_normals();
    }
}


// µ±´°Ìå¸Ä±ä´óÐ¡µÄÊ±ºò
void myReshape(GLint w, GLint h)
{
    glViewport(0, 0, static_cast<GLsizei>(w), static_cast<GLsizei>(h));
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    if (w > h)
        glOrtho(-static_cast<GLdouble>(w) / h, static_cast<GLdouble>(w) / h, -1.0, 1.0, -100.0, 100.0);
    else
        glOrtho(-1.0, 1.0, -static_cast<GLdouble>(h) / w, static_cast<GLdouble>(h) / w, -100.0, 100.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

void myDisplay()
{
	//minus_range_x=0;
	//minus_range_y=0;
	//minus_range_z=0;
    if(flag){
		ofstream outfile;
	    outfile.open(image_txt,ios::out);
        for(int i=0;i<=range_x;i++)
        {
           
            for(int j=0;j<=range_y;j++)
            {
                
                for(int k=0;k<=range_z;k++)
                {
					xRotate=xNum*1.0/10;
					yRotate=yNum*1.0/10;
					zRotate=zNum*1.0/10;

					
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                    glLoadIdentity();
 
                    //ÓëÏÔÊ¾Ïà¹ØµÄº¯Êý
           
                    glRotatef(xRotate, 1.0f, 0.0f, 0.0f); // ÈÃÎïÌåÐý×ªµÄº¯Êý µÚÒ»¸ö²ÎÊýÊÇ½Ç¶È´óÐ¡£¬ºóÃæµÄ²ÎÊýÊÇÐý×ªµÄ·¨ÏòÁ¿
                    glRotatef(yRotate, 0.0f, 1.0f, 0.0f);
                    glRotatef(zRotate, 0.0f, 0.0f, 1.0f);
                    glTranslatef(0.0f, -0.35, 0.0f);
                    glScalef(scale, scale, scale); // Ëõ·Å
                    //Ã¿´Îdisplay¶¼ÒªÊ¹ÓÃglcalllist»Øµ÷º¯ÊýÏÔÊ¾ÏëÏÔÊ¾µÄ¶¥µãÁÐ±í
                    glCallList(showFaceList);
                    glutSwapBuffers(); //ÕâÊÇOpenglÖÐÓÃÓÚÊµÏÖË«»º´æ¼¼ÊõµÄÒ»¸öÖØÒªº¯Êý
					
                    char* pName=new char[20];
                    createName(xRotate,yRotate,zRotate,pName);
					outfile<<(pName)<<endl;
					char *fName=new char[30];
					createFileName(pName,fName);
                    grab(fName);
                    zNum=zNum+step;
                }
                yNum=yNum+step;
                zNum=minus_range_z;
            }
            xNum=xNum+step;
            yNum=minus_range_y;
        }
		outfile.close();
    }
    flag=0;
}


int main(int argc, char** argv)
{

		char *cmd=new char[30];
		int j=0;
		cmd[j++]='"';
		cmd[j++]='m';
		cmd[j++]='k';
		cmd[j++]='d';
		cmd[j++]='i';
		cmd[j++]='r';
		cmd[j++]=' ';
		
		for(int k=0;k<strlen(dirTrain);k++)
		{
			cmd[j++]=dirTrain[k];
		}
		
		cmd[j++]='"';
		cmd[j++]='\0';
		system(cmd);

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH); // GLUT_Double ±íÊ¾Ê¹ÓÃË«»º´æ¶ø·Çµ¥»º´æ
    glutInitWindowPosition(0, 0);
    glutInitWindowSize(WIDTH, HEIGHT);
    glutCreateWindow("Mesh Viewer");
    readfile(file_1);
    initGL();
    glutReshapeFunc(&myReshape);
    //glutIdleFunc(&myIdle);
    glutDisplayFunc(&myDisplay);

    glutMainLoop();
    return 0;
}