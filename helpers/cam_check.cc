#include <opencv2/opencv.hpp>
#include "stdio.h"

const char STREAM_URL[] = "http://10.0.0.4:8080/video?x.mjpeg";

int main(void){

    cv::VideoCapture camera;
    camera.open(STREAM_URL);

    if (camera.isOpened()==true)
    {
        cv::namedWindow("camera");
        int key = 0;
        while (key != 27)
        {
            cv::Mat_<cv::Vec3b> image;        
            camera.grab();
            camera.retrieve(image);
            cv::imshow("camera",image);
            key = cv::waitKey(10);
        }
    }
		else{ printf("\nCAM_CHECK : STREAM_URL %s not opening\nCheck variable STREAM_URL @l4\n",STREAM_URL);}

		return 0;
}
