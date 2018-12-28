#include <iostream>  
#include <OpenMesh/Core/IO/MeshIO.hh>  
#include <OpenMesh/Core/Mesh/TriMesh_ArrayKernelT.hh>  
#include "GL\glut.h"
#include <math.h>
#include <Windows.h>
#include <string>
#include <sstream>
#include <fstream> 
#include<stdio.h>
#include<FreeImage.h> 

//#pragma comment(lib,"FreeImage.lib")

using namespace std;
typedef OpenMesh::TriMesh_ArrayKernelT<> MyMesh;


//与实现角度大小相关的参数，
float xRotate = 0;
float yRotate = 0;
float zRotate = 0;




//文件读取有关的
MyMesh mesh;
const string file_1 = "2rt.off";

//用于display函数
int flag=1;

GLuint showFaceList, showWireList;
int showstate = 1;
bool showFace = true;
bool showWire = false;
bool showFlatlines = false;



//窗口大小
int winSize=900;
FIBITMAP* bitmap; 
unsigned char *mpixels; 
float *scales;
float scale;

int first=0;

void grab(char *pName,int picSize)
{
    //int offset=(winSize-picSize)/2;
    glReadBuffer(GL_FRONT);
    glReadPixels(0, 0, picSize, picSize, GL_RGB, GL_UNSIGNED_BYTE, mpixels);
    glReadBuffer(GL_BACK);
    for(int i = 0; i < (int)picSize*picSize*3; i += 3)
    {   
        mpixels[i] ^= mpixels[i+2] ^= mpixels[i] ^= mpixels[i+2];
    }
 
    for(int y = 0 ; y < FreeImage_GetHeight(bitmap); y++)
    {
        BYTE *bits = FreeImage_GetScanLine(bitmap, y);
        for(int x = 0 ; x < FreeImage_GetWidth(bitmap); x++)
        {
            bits[0] = mpixels[(y*picSize+x) * 3 + 0];
            bits[1] = mpixels[(y*picSize+x) * 3 + 1];
            bits[2] = mpixels[(y*picSize+x) * 3 + 2];
            bits += 3;
        }
 
    }

    FreeImage_Save(FIF_JPEG, bitmap, pName, JPEG_DEFAULT);

}

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


void createFileName(char*fName,char* pName)
{
    int t=strlen(fName);
    fName[t++]='\\';
    for(int i=0;i<strlen(pName);i++)
    {

        fName[t++]=pName[i];
    }
    fName[t++]='\0';

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
double randf() 
{ 
    double r=(double)(rand()%10001);
    r=r*1.0/1000-5;
    return r; 
} 
void myDisplay()
{
    srand((int)time(0));//使用系统时间作为随机种子
    if(flag){
        ofstream outfile;
        outfile.open("image_test.txt",ios::out);
        for(int i=0;i<2000;i++)
        {
        
            xRotate=randf();
            yRotate=randf();
            zRotate=randf();
            char* pName=new char[20];
            createName(xRotate,yRotate,zRotate,pName);
            outfile<<(pName)<<endl;

            for(int t=0;t<11;t++)
            {
                char* fName=new char[30];
                sprintf(fName, "%d", t);
                createFileName(fName,pName);
                scale=scales[t];
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                glLoadIdentity();
     
                //与显示相关的函数
                glRotatef(xRotate, 1.0f, 0.0f, 0.0f); // 让物体旋转的函数 第一个参数是角度大小，后面的参数是旋转的法向量
                glRotatef(yRotate, 0.0f, 1.0f, 0.0f);
                glRotatef(zRotate, 0.0f, 0.0f, 1.0f);
                glTranslatef(0.0f, -0.35, 0.0f);
                glScalef(scale, scale, scale); // 缩放
                       
                //每次display都要使用glcalllist回调函数显示想显示的顶点列表
        
                glCallList(showFaceList);
                glutSwapBuffers(); //这是Opengl中用于实现双缓存技术的一个重要函数
                grab(fName,winSize);
                //free(fName);

            }
           // free(pName);

        }
        outfile.close();
    }


    flag=0;
    
}



int main(int argc, char** argv)
{
    scales=new float[5];
    double init=0.012;
    for(int i=0;i<5;i++)
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
        cmd[j++]='.';
        cmd[j++]='\\';
        char *file=new char[10];
        sprintf(file,"%d",i);
        for(int k=0;k<strlen(file);k++)
        {
            cmd[j++]=file[k];
        }
        cmd[j++]='"';
        cmd[j++]='\0';
        system(cmd);
        //free(file);
        //free(cmd);
        scales[i]=init+0.004*i;
    }
    bitmap= FreeImage_Allocate(winSize, winSize, 24, 8, 8, 8);
    mpixels= new unsigned char[winSize * winSize * 3];

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH); // GLUT_Double 表示使用双缓存而非单缓存
    glutInitWindowPosition(100, 100);
    glutInitWindowSize(winSize, winSize);
    glutCreateWindow("Mesh Viewer");
    readfile(file_1);
    initGL();
    glutReshapeFunc(&myReshape);
    //glutIdleFunc(&myIdle);
    glutDisplayFunc(&myDisplay);

    glutMainLoop();
    return 0;
    
}