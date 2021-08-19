import cv2
import FastFunctions as Fast
from time import sleep
cap =cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
pos = [
'G0 E0 X239 F10000',
'G0 E90 X238 F10000',
'G0 E90 X258 F10000',
'G0 E180 X261 F10000',
'G0 E270 X265 F10000',
'G0 E270 X238 F10000']
_,__, a = Fast.SerialConnect(SerialPath="Json/serial.json", name="Ramps 1.4")
comb = ["G0 X14 f10000", "G0 Y31 F1000", "M42 P31 S255", "G28 Y", "M42 p34 s255"]


for cc in comb:
	Fast.sendGCODE(a, cc)
	Fast.M400(a)
ss = 0

for pp in pos:
	ss += 1
	Fast.sendGCODE(a, pp)
	Fast.M400(a)
	sleep(1)
	for _ in range(5):
		img = cap.read()[1]
		cv2.imshow("img", cv2.resize(img,None, fx=0.5, fy=0.5))
	cv2.imwrite(f"/home/pi/Desktop/frame_{ss}.jpg", img)