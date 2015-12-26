import cv2
import numpy as np
import socket
import sys


# In[ ]:
IP = '192.168.0.2'
PORT = 10001

# datset name
DNAME = "./follow_selva_01.pkl"




# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (IP, PORT)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

# global frame count
frame_count = 0



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
frame_count = 0
message='q' 
one_hot  = -1
ack = -1
i=0



def get_mouse_event(event,x,y,flags,param):

    global sample
    global que
    global datasetX
    global datasetY
    global one_hot

    if event == cv2.EVENT_LBUTTONDOWN:
        gridx,gridy = (int(x/96),int(y/54))
        one_hot = (gridx) + (gridy * 5) - 10
        print 'One hot : %d'%(one_hot) 
        if one_hot > -1 and one_hot < 15:
            message="(%d)"%(one_hot)
            print >>sys.stderr, 'sending "%s"' % message
            sock.sendall(message)
            # add to sample
            sample.append(np.asarray(que[0]).ravel())
            sample.append(np.asarray(que[2]).ravel())
            sample.append(np.asarray(que[3]).ravel())
            sample.append(cv2.blur(que[-1],(5,5)).ravel())
            sample.append(cv2.filter2D(que[-2], -1, kernel).ravel())

            datasetX.append(sample)
            datasetY.append(one_hot)
            print '\nsample : stored'
            sample = [ ]
            one_hot = -1

cap = cv2.VideoCapture("http://192.168.0.3:8080/video?x.mjpeg")
cv2.namedWindow('frame')
cv2.setMouseCallback('frame',get_mouse_event)











while True:
    
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

    cv2.imshow('frame',resized)

    k = cv2.waitKey(20) & 0xFF
    if k == 27:        
        break

    '''
    # construct message of form (l,r)
    if one_hot > -1 and one_hot < 15:
        message="(%d)"%(one_hot)
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
        one_hot = -1

    else:
        continue
    
    if one_hot > -1:
        ack = connection.recv(16)	
        one_hot = -1

    if ack != 'ack':
        continue 


    if one_hot == -1:
        continue

    one_hot = -1
    # add to sample
    sample.append(np.asarray(que[0]).ravel())
    sample.append(np.asarray(que[2]).ravel())
    sample.append(np.asarray(que[3]).ravel())
    sample.append(cv2.blur(que[-1],(5,5)).ravel())
    sample.append(cv2.filter2D(que[-2], -1, kernel).ravel())

    datasetX.append(sample)
    datasetY.append()
    print '\nsample : %d stored'%(i)
    i = i+1
    sample = [ ]
    '''

import pickle
pickle.dump((datasetX, datasetY), open( DNAME, "wb" ) )  

cv2.destroyAllWindows()
