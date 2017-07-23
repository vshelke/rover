import serial, socket

IP = "192.168.1.21"
PORT = 23907

#BIO_DATA = "pp.pp,cccc,tt.t,hh"

arduino = serial.Serial('/dev/ttyBIO', 9600)
station = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	while True:
        	DATA = arduino.readline()
        	station.sendto(DATA, (IP, PORT))
except:
	station.close()
