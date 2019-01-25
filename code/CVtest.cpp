#include <cv.h>
#include <cxcore.h>
#include <highgui.h>
#include <iostream>
#include "opencv2/opencv.hpp"

#include "core/core.hpp"  
#include "highgui/highgui.hpp"  
#include "imgproc/imgproc.hpp"  
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
 
using namespace std;
using namespace cv;

RNG rng;

//裁剪图片
void cut_X()
{
	Mat src;
	src = imread("test2.jpg");
	Rect rect(300,300,700,700);
	Mat dst=src(rect);
	imwrite("lena.jpg",dst);
					
}


//对X光片进行处理
void X()
{
    Mat src = imread("test.jpg");
    Rect rect(0,0,364,313);//左上坐标（X,Y）和长宽
    Mat result, bg, fg;
    grabCut(src, result, rect, bg, fg, 1, GC_INIT_WITH_RECT);
    imshow("grab", result);
	imwrite("test1.jpg",result);
    compare(result, GC_PR_FGD, result, CMP_EQ);//result和GC_PR_FGD对应像素相等时，目标图像该像素值置为255
    imshow("result",result);
	imwrite("test2.jpg",result);
    Mat foreground(src.size(), CV_8UC3, Scalar(255, 255, 255));
    src.copyTo(foreground, result);//copyTo有两种形式，此形式表示result为mask
    imshow("foreground", foreground);
	imwrite("test3.jpg",foreground);



    waitKey(0);
}


void cut(char* src)
{
	Mat image=imread(src,1);
	Mat gray;
	cvtColor(image,gray,CV_BGR2GRAY);
	//imshow("gray",gray);
	imwrite("gray.jpg",gray);
	Mat thresh;
	threshold(gray,thresh,50,255,THRESH_BINARY);
	//imshow("thresh",thresh);
	imwrite("thresh.jpg",thresh);

	Mat grad_x, grad_y;
	Mat abs_grad_x, abs_grad_y,dst;
 

	Sobel( thresh, grad_x, CV_16S, 1, 0, 3, 1, 1, BORDER_DEFAULT );
	convertScaleAbs( grad_x, abs_grad_x );
	
	Sobel( thresh, grad_y, CV_16S, 0, 1, 3, 1, 1, BORDER_DEFAULT );
	convertScaleAbs( grad_y, abs_grad_y );
	
	addWeighted( abs_grad_x, 0.5, abs_grad_y, 0.5, 0, dst );
	
	imwrite(src,dst);
	vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
	findContours( dst, contours, hierarchy, CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE);

	int idx = 0;
    for( ; idx >= 0; idx = hierarchy[idx][0] )
    {
        Scalar color( rand()&255, rand()&255, rand()&255 );
        drawContours( dst, contours, idx, color, CV_FILLED, 8, hierarchy );
    }

    namedWindow( "Components", 1 );
    imshow( "Components", dst );
	waitKey(0);
	
}
 
void findContours(char *imgPath)
{
	Mat src;
    // the first command-line parameter must be a filename of the binary
    // (black-n-white) image
   
	src=imread(imgPath, 0);
    Mat dst = Mat::zeros(src.rows, src.cols, CV_8UC3);

    src = src > 1;
    namedWindow( "Source", 1 );
    imshow( "Source", src );

    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;

    findContours( src, contours, hierarchy,
        CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE );

    // iterate through all the top-level contours,
    // draw each connected component with its own random color
    int idx = 0;
    for( ; idx >= 0; idx = hierarchy[idx][0] )
    {
        Scalar color( rand()&255, rand()&255, rand()&255 );
        drawContours( dst, contours, idx, color, CV_FILLED, 8, hierarchy );
    }

    namedWindow( "Components", 1 );
    imshow( "Components", dst );
    waitKey(0);
	

	
}
void contour(char* src)
{
	IplImage* image = cvLoadImage(src,1);
	CvMemStorage* storage1 = cvCreateMemStorage();
	CvSeq* contour1 = NULL;
	int Nc1= cvFindContours(image,storage1,&contour1,sizeof(CvContour),CV_RETR_EXTERNAL);
	cout<<Nc1<<endl;//最后一个参数的可变性

}
int main()
{
	X();
	return 0;
}