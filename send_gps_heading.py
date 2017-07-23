import gps, hmc5883l, socket

IP = "192.168.1.118"
PORT = 3301

compass = hmc5883l.hmc5883l(gauss=4, declination=(-1,17))
gpsd = gps.gps(mode = gps.WATCH_ENABLE)
station = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	while 1:
		HEAD = compass.heading()
		HEAD = 359 - HEAD % 360
		LAT = gpsd.fix.latitude
		LON = gpsd.fix.longitude
		DATA = "$," + str(LAT) + "," + str(LON) + "," + str(int(HEAD)) + ",0,0,#,"
		print DATA
		station.sendto(DATA, (IP, PORT))  
		gpsd.next()

except:
	station.close()
