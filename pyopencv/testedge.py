#!/usr/bin/python
from opencv.cv import *
from opencv.highgui import *

def process_and_draw( img, noise ):
  # create the output image
  col_edge = cvCreateImage (cvSize (img.width, img.height), 8, 3)

  # convert to grayscale
  gray = cvCreateImage (cvSize (img.width, img.height), 8, 1)
  edge = cvCreateImage (cvSize (img.width, img.height), 8, 1)
  cvCvtColor (img, gray, CV_BGR2GRAY)

  # Subtract noise profile (ie: last image)
#  gray -= noise
  
  cvSmooth (gray, edge, CV_BLUR, 3, 3, 0)
  cvNot (gray, edge)

  # run the edge dector on gray scale
  cvCanny (gray, edge, 120, 150, 3)

  # reset
  cvSetZero (col_edge)

  # copy edge points
  cvCopy (img, col_edge, edge)
  
  # display image
  cvShowImage( "result", col_edge )

if __name__ == '__main__':
  # open capture device and grab first frame
  input_name = 0
  capture = cvCreateCameraCapture( int(input_name) )
  frame = cvQueryFrame( capture );

  # create windows
  cvNamedWindow( "result", 1 )

  # initialize
  frame_copy = cvCreateImage( cvSize(frame.width,frame.height),IPL_DEPTH_8U, frame.nChannels )
  noise = cvCreateImage( cvSize(frame.width,frame.height), 8, 1 )
  cvCvtColor(frame, noise, CV_BGR2GRAY)

  # get new frames, edge detect and display
  while True: 
      frame = cvQueryFrame( capture );
      if( not frame ):
          break
      if( frame.origin == IPL_ORIGIN_TL ):
          cvCopy( frame, frame_copy )
      else:
          cvFlip( frame, frame_copy, 0 );
      process_and_draw(frame_copy,noise)
      if( cvWaitKey( 10 ) >= 0 ):
          break;
      cvCvtColor(frame, noise, CV_BGR2GRAY)
  cvDestroyWindow("result")
