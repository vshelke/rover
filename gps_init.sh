sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
sleep 1
sudo ps -aux | grep gpsd
echo "GPSD started :) "
