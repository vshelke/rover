import gps, serial, socket, time, math, hmc5883l

def initalize(ino):
    # http://magnetic-declination.com/
    compass = hmc5883l.hmc5883l(gauss=4, declination=(-1,17))
    gpsd = gps.gps(mode = gps.WATCH_ENABLE)
#    arduino = serial.Serial(ino, 38400)
    station = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    station.bind(("0.0.0.0", 3301))
    return (compass, gpsd, arduino, station)

def update_gps(gpsd):
    """gps update speed(m/sec) - extra variables: gpsd.fix.climb, gpsd.fix.track"""
    gpsd.next()
    return (gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.satellites, gpsd.fix.speed)

def update_compass(compass):
    """gets the current heading from the compass"""
    return compass.heading()

def lerp(x, in_min, in_max, out_min, out_max):
    """arduino lerp function"""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def make_packet(l, r):
    l = lerp(l, -100, 100, 1, 127)
    r = lerp(r, -100, 100, 1, 127)
    return chr(174)+chr(l)+chr(r)+chr(175)

def constrain(x, low, high):
    """arduino constrain function"""
    if x > high:
        return high
    elif x < low:
        return low
    else:
        return x

def get_bearing(lat1, lon1, lat2, lon2):
    """computes the true angle between the coordinates w.r.t (north)"""
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

def get_distance(lat1, lon1, lat2, lon2):
    """computes the distance between two coordinates in (meters)"""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lam = math.radians(lon2 - lon1)
    a = math.sin(d_phi/2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371000 * c

def smooth(o_l, o_r, c_l, c_r, AMT):
    """alpha filter to smooth the motor output"""
    l  =  o_l * AMT  + (1-AMT) * c_l
    r  =  o_r * AMT  + (1-AMT) * c_r
    return (l, r)
