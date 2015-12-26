import cv2
import numpy as np
import socket
import sys


# mouse callback function
def get_mouse_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print "mouse click (%d,%d)"%(x,y)
        print 'GRID : (%d,%d)'%(int(x/96),int(y/54))

cv2.namedWindow('frame')
cv2.setMouseCallback('frame',get_mouse_event)

im = cv2.imread('~/Pictures/011.jpg')
cv2.imshow('frame',im)

cv2.waitKey(-1)

cv2.destroyAllWindows()
