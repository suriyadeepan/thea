import Adafruit_BBIO.GPIO as gpio
import Adafruit_BBIO.PWM as PWM
from time import sleep

# socket server
import socket
import sys

PORT = 10000

def halt():
	gpio.output(a, gpio.LOW)
	gpio.output(b, gpio.LOW)
	gpio.output(d, gpio.LOW)
	gpio.output(c, gpio.LOW)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', PORT)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    if not (client_address is None):
        break
print >>sys.stderr, 'connection from', client_address

# GPIO setup
a="P8_19"
b="P8_13"
c='P9_16'
d='P9_14'

#gpio.setup(a,gpio.OUT)
gpio.setup(b,gpio.OUT)
#gpio.setup(c,gpio.OUT)
gpio.setup(d,gpio.OUT)

PWM.start(a, 0, 1000)
PWM.start(c, 0, 1000)
#sleep(3)
#print 'running @ 99%'
#PWM.set_duty_cycle("P8_13", 99)
#sleep(3)

while(True):
	inq = connection.recv(16)	
	# __Message Format___ : "(left_state,right_state)"
	print '\nBB > Raw :', inq
	if len(inq) <= 7 and len(inq) >= 5:
		le,ri = inq[1:-1].split(',')	
		print '\nBB > (%d,%d)'%(int(le),int(ri))
		PWM.set_duty_cycle(a,int(le))
		PWM.set_duty_cycle(c,int(ri))
	
	
gpio.cleanup()

print 'stopping now'
PWM.stop(a)
PWM.stop(c)

PWM.cleanup()
