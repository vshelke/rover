import autobot, time, sys

TARGET = [12.821139, 80.038193]
CURRENT = [0.0, 0.0]
HEADING = 0
BEARING = 0
DISTANCE = 0
LEFT = 0
RIGHT = 0
THRESH = int(sys.argv[1])
DIST_THRESH = int(sys.argv[2])
IP = "192.168.1.21"
waypoint = 0
path = []
ctr = 0

def make_way(station):
    data, addr = station.recvfrom(1024)
    way = []
    while data != "<end>":
        s = data.split(",")
        if s[0] == '<' and s[4] == '>':
            way.insert(int(s[1]), [float(s[2]), float(s[3])])
        data, addr = station.recvfrom(1024)
    return way

def magic(l, r):
    l = int(autobot.lerp(l, -180, 180, -70, 70))
    r = int(autobot.lerp(r, -180, 180, -70, 70))
    return (l, r)

if __name__ == "__main__":
    compass, gpsd, arduino, station = autobot.initalize('/dev/ttyUSB1')
    print("waiting for way points")
    path = make_way(station)
    waypoint = 0
    print("initializing...")
    TARGET = path[waypoint]
    try:
    	while True:
            CURRENT[0], CURRENT[1], _, _, _ = autobot.update_gps(gpsd)
            HEADING = autobot.update_compass(compass)
            HEADING = 359 - HEADING % 360
            BEARING = autobot.get_bearing(CURRENT[0], CURRENT[1], TARGET[0], TARGET[1])
            DISTANCE = autobot.get_distance(CURRENT[0], CURRENT[1], TARGET[0], TARGET[1])
            data = "$,"+str(CURRENT[0])+","+str(CURRENT[1])+","+str(int(HEADING))+","+str(int(BEARING))+","+str(int(DISTANCE))+",#,"
            station.sendto(data, (IP, 3301))
            if ctr < 10:
		        ctr = ctr + 1
		        continue
            if DISTANCE < DIST_THRESH:
                print "Distance rec ", DISTANCE
                waypoint = waypoint + 1
                TARGET = path[waypoint]
                ctr = 0
                station.sendto("M,"+str("WayPoint Reached. Hit 'Next'", (IP, 3301))
                data, addr = station.recvfrom(1024)
                continue
            error = int(BEARING - HEADING)
            if abs(error) > 180:
		        error = (360 - error)%360
                if abs(error) < THRESH:
                    LEFT = 60 - error
			        RIGHT = 60 + error
		        else:
			        LEFT = -error
			        RIGHT = error
	        else:
		        if abs(error) < THRESH:
			        LEFT = 60 + error
			        RIGHT = 60 - error
		        else:
			        LEFT = error
			        RIGHT = -error
            LEFT, RIGHT = magic(LEFT, RIGHT)
            #print "BEAR " , BEARING , " HEAD " , HEADING , " DIST " , DISTANCE , " ERR " , error , " LEFT " , LEFT , " RIGHT " , RIGHT
            arduino.write(autobot.make_packet(LEFT, RIGHT))
            time.sleep(0.1)
    except KeyboardInterrupt:
            arduino.write(autobot.make_packet(0, 0))
            pass
