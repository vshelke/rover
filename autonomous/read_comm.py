import socket


IP = "192.168.1.21"
station = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
station.bind(("0.0.0.0", 3301))


path = []

def make_way(station):
    data, addr = station.recvfrom(1024)
    way = []
    while data != "<end>":
        s = data.split(",")
        if s[0] == '<' and s[4] == '>':
            way.insert(int(s[1]), [float(s[2]), float(s[3])])
        data, addr = station.recvfrom(1024)
    return way

while 1:
    print "going in reading mode"
    path = make_way(station)
    print path
    station.sendto("M,"+str(len(path))+" packets recived", (IP, 3301))
