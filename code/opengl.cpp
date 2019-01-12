
typedef OpenMesh::TriMesh_ArrayKernelT<> MyMesh;


//文件读取有关的
MyMesh mesh;

GLuint showFaceList, showWireList;
int showstate = 1;
bool showFace = true;
bool showWire = false;
bool showFlatlines = false;

int WIDTH=900,HEIGHT=900;

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
 
                    //与显示相关的函数
           
                    glRotatef(xRotate, 1.0f, 0.0f, 0.0f); // 让物体旋转的函数 第一个参数是角度大小，后面的参数是旋转的法向量
                    glRotatef(yRotate, 0.0f, 1.0f, 0.0f);
                    glRotatef(zRotate, 0.0f, 0.0f, 1.0f);
                    glTranslatef(0.0f, -0.35, 0.0f);
                    glScalef(scale, scale, scale); // 缩放
                    //每次display都要使用glcalllist回调函数显示想显示的顶点列表
                    glCallList(showFaceList);
                    glutSwapBuffers(); //这是Opengl中用于实现双缓存技术的一个重要函数
					
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

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH); // GLUT_Double 表示使用双缓存而非单缓存
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