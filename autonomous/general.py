qimport serial, socket, gps, hmc5883l

IP = "192.168.1.21"
PORT = 3301

def initalize(ino):
    # http://magnetic-declination.com/
    compass = hmc5883l.hmc5883l(gauss=4, declination=(-1,17))
    gpsd = gps.gps(mode = gps.WATCH_ENABLE)
    arduino = serial.Serial(ino, 9600)
    station = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return (compass, gpsd, arduino, station)

def update_gps(gpsd):
    gpsd.next()
    return (gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.satellites, gpsd.fix.speed)

def update_compass(compass):
    """gets the current heading from the compass"""
    return compass.heading()

if __name__ == "__main__":
    compass, gpsd, arduino, station = initalize('dev/ttyTSK')

    try:
    	while True:
            LAT, LON, ALT, SAT, SPD = update_gps(gpsd)
            HEAD = autobot.update_compass(compass)
            HEAD = 359 - HEAD % 360
            DATA = "#"+str(LAT)+str(LON)+str(HEAD)+str(ALT)+str(SAT)+str(SPD)+"%"
            station.sendto(DATA, (IP, PORT))
    except KeyboardInterrupt:
    	station.close()
