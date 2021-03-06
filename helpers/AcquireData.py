import cv2
import numpy as np
import socket
import sys


# In[ ]:
IP = '192.168.0.2'
PORT = 10000

# datset name
DNAME = "../../data/hcb01.pkl"

# mouse callback function
def get_mouse_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print "mouse click (%d,%d)"%(x,y)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (IP, PORT)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

# global frame count
frame_count = 0


#cap = cv2.VideoCapture("http://10.0.0.7:8080/video?x.mjpeg")
cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')
cv2.setMouseCallback('frame',get_mouse_event)


# kernel for sharpen operation
kernel = np.zeros( (8,8), np.float32); kernel[4,4] = 2.0 
#Create a box filter:
boxFilter = np.ones( (8,8), np.float32) / 81.0
#Subtract the two:
kernel = kernel - boxFilter

datasetX = [] # [list of 6x270x480 images]
datasetY = [] # (one hot vector of most traversible region)
sample = []
que = []
i=0
frame_count = 0
message='q' 
while(frame_count < 1500):
    
    ret, frame = cap.read()
    
    if frame is None:
        print "frame is none; breaking"
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray,(480,270), interpolation = cv2.INTER_CUBIC)

    # add to queue
    if len(que) > 5:
        del que[0]
    else:
        que.append(resized)

    cv2.imshow('frame',frame)

    cv2.waitKey(10)
            
    # construct message of form (l,r)
    message="(%s,%s)"%(l.get_value(),r.get_value())
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    
	ack = connection.recv(16)	

    if ack != 'ack':
        continue 

    # add to sample
    sample.append(np.asarray(que[0]).ravel())
    sample.append(np.asarray(que[2]).ravel())
    sample.append(np.asarray(que[3]).ravel())
    sample.append(cv2.blur(que[-1],(5,5)).ravel())
    sample.append(cv2.filter2D(que[-2], -1, kernel).ravel())

    datasetX.append(sample)
    datasetY.append()

    i = i+1
    frame_count = frame_count + 1
    if i > 5:
        sample = []
        i = 0

import pickle
pickle.dump((datasetX, datasetY), open( DNAME, "wb" ) )  

cv2.destroyAllWindows()
