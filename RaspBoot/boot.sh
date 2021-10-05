echo Iniciando o Back
sleep 2
lxterminal --geometry=80x25 --title=Back -e bash -c  '/home/pi/Desktop/RaspBoot/Back.sh'
echo Iniciando o Front
sleep 2
lxterminal --geometry=80x25 --title=Front -e bash -c  '/home/pi/Desktop/RaspBoot/Front.sh'
echo Fim
sleep 1
