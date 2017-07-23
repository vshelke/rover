import serial, time
s = serial.Serial('/dev/cu.usbserial', 38400)

def lerp(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def make_packet(l, r):
    l = lerp(l, -100, 100, 1, 127)
    r = lerp(r, -100, 100, 1, 127)
    return chr(174)+chr(l)+chr(r)+chr(175)

while 1:
    # st = raw_input('>')
    # tmp = st.split(',')
    for i in range(-100, 100):
        s.write(make_packet(i, i))
        time.sleep(0.1)
