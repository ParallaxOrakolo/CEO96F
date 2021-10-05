sleep 3
echo home_Desktop_Github_CEO96F
#sleep 1
cd /home/pi/Desktop/Gihub/CEO96F/dist
#echo export RAM
#sleep 1
#export NODE_OPTIONS=--max_old_space_size=4096
#
echo run Server
sleep 1
source /home/pi/.virtualenvs/opencv4.4/bin/activate
python -m http.server
$SHELL
sleep 10