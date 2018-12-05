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



//设置角度范围
int range=10;
//设置步长
float step =0.2;

int range_min=0;
//与实现角度大小相关的参数，
float xRotate = range_min*1.0;
float yRotate = range_min*1.0;
float zRotate = range_min*1.0;
float ty = 0.0f;
//float scale = 0.0145;
float scale=0.02;


//文件读取有关的
MyMesh mesh;
const string file_1 = "newtest.off";

int flag=1;

GLuint showFaceList, showWireList;
int showstate = 1;
bool showFace = true;
bool showWire = false;
bool showFlatlines = false;

int WIDTH=800,HEIGHT=800;
FIBITMAP* bitmap = FreeImage_Allocate(WIDTH, HEIGHT, 24, 8, 8, 8);
unsigned char *mpixels = new unsigned char[WIDTH * HEIGHT * 3];

int first=0;
//初始化顶点和面   
void initGL()
{
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glClearDepth(2.0);
    glShadeModel(GL_SMOOTH);
   
    showFaceList = glGenLists(1);
    showWireList = glGenLists(1);
    int temp = mesh.n_edges();

    // 绘制 wire 
    glNewList(showWireList, GL_COMPILE);
  
    glLineWidth(1.0f);
    glColor3f(1.0f, 1.0f, 1.0f);
    glBegin(GL_LINES);
    for (MyMesh::HalfedgeIter he_it = mesh.halfedges_begin(); he_it != mesh.halfedges_end(); ++he_it) {
        //链接这个有向边的起点和终点
        glVertex3fv(mesh.point(mesh.from_vertex_handle(*he_it)).data());
        //cout<<mesh.point(mesh.from_vertex_handle(*he_it)).data()<<endl;
        glVertex3fv(mesh.point(mesh.to_vertex_handle(*he_it)).data());
    }
    glEnd();
    glEndList();

    // 绘制flat
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
    if(strlen(xx)<3)
    {
        n[i++]='.';
        n[i++]='0';
    }
    n[i++]='_';
    char*yy=new char[20];
    sprintf(yy, "%g", y);
    for(int j=0;j<strlen(yy);j++)
    {
        n[i++]=yy[j];
    }
    if(strlen(yy)<3)
    {
        n[i++]='.';
        n[i++]='0';
    }
    n[i++]='_';
    char*zz=new char[20];
    sprintf(zz, "%g", z);
    for(int j=0;j<strlen(zz);j++)
    {
        n[i++]=zz[j];
    }
    if(strlen(zz)<3)
    {
        n[i++]='.';
        n[i++]='0';
    }
    n[i++]='.';
    n[i++]='j';
    n[i++]='p';
    n[i++]='g';
    n[i++]='\0';

}


void grab(char *pName)
{
    
    glReadBuffer(GL_FRONT);
    glReadPixels(160, 200, WIDTH, HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, mpixels);
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


// 读取文件的函数
void readfile(string file) {
    // 请求顶点法线 vertex normals
    mesh.request_vertex_normals();
    //如果不存在顶点法线，则报错 
    if (!mesh.has_vertex_normals())
    {
        cout << "错误：标准定点属性 “法线”不存在" << endl;
        return;
    }
    // 如果有顶点发现则读取文件 
    OpenMesh::IO::Options opt;
    if (!OpenMesh::IO::read_mesh(mesh, file, opt))
    {
        cout << "无法读取文件:" << file << endl;
        return;
    }
    else cout << "成功读取文件:" << file << endl;
    cout << endl; 

    if (!opt.check(OpenMesh::IO::Options::VertexNormal))
    {
        // 通过面法线计算顶点法线
        mesh.request_face_normals();
        // mesh计算出顶点法线
        mesh.update_normals();
        // 释放面法线
        mesh.release_face_normals();
    }
}


// 当窗体改变大小的时候
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
    if(flag){
        for(int i=0;i<range;i++)
        {
           
            for(int j=0;j<range;j++)
            {
                
                for(int k=0;k<range;k++)
                {
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                    glLoadIdentity();
 
                    //与显示相关的函数
           
                    glRotatef(xRotate, 1.0f, 0.0f, 0.0f); // 让物体旋转的函数 第一个参数是角度大小，后面的参数是旋转的法向量
                    glRotatef(yRotate, 0.0f, 1.0f, 0.0f);
                    glRotatef(zRotate, 0.0f, 0.0f, 1.0f);
                    glTranslatef(0.0f, 0.0f, ty);
                    glScalef(scale, scale, scale); // 缩放
                    //每次display都要使用glcalllist回调函数显示想显示的顶点列表
                    glCallList(showFaceList);
                    glutSwapBuffers(); //这是Opengl中用于实现双缓存技术的一个重要函数
                    char* pName=new char[30];
                    createName(xRotate,yRotate,zRotate,pName);
                    grab(pName);
                    zRotate=zRotate+step;
                }
                yRotate=yRotate+step;
                zRotate=range_min*1.0;
            }
            xRotate=xRotate+step;
            yRotate=range_min*1.0;
        }
    }
    flag=0;
}


int main(int argc, char** argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH); // GLUT_Double 表示使用双缓存而非单缓存
    glutInitWindowPosition(100, 100);
    glutInitWindowSize(1024, 1024);
    glutCreateWindow("Mesh Viewer");
    readfile(file_1);
    initGL();
    glutReshapeFunc(&myReshape);
    //glutIdleFunc(&myIdle);
    glutDisplayFunc(&myDisplay);

    glutMainLoop();
    return 0;
}