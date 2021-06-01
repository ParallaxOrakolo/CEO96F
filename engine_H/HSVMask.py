import FastFunctions as Fast
import OpencvPlus as Op
import cv2
import numpy as np


def findCircle(circle_Mask, areaMinC, areaMaxC, perimeter_size, blur_Size=3):
    circle_info = []
    blur = cv2.medianBlur(circle_Mask, blur_Size)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    edges = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edges = edges[0] if len(edges) == 2 else edges[1]
    for c in edges:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(c)
        if len(approx) > perimeter_size and areaMinC < area < areaMaxC:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            circle_info.append({"center": (x, y), "radius": r})
    return circle_info

def findHole(imgAnalyse, minArea, maxArea, c_perimeter, lower, upper):

    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    mask = Op.refineMask(Op.HSVMask(imgAnalyse, lower, upper))
    cv2.imshow("Mask", mask)
    chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
    
    distances = []
    edge = findCircle(mask, minArea, maxArea, c_perimeter)
    for Circle in edge:
        cv2.circle(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), int(Circle['radius']),
                   (36, 255, 12), 2)

        cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), fixPoint, (168, 50, 131))

        cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])),
                 (int(Circle['center'][0]), fixPoint[1]), (255, 0, 0))

        cv2.line(chr_k, (int(Circle['center'][0]), fixPoint[1]), fixPoint, (0, 0, 255), thickness=2)

        distance_to_fix = (round((Circle['center'][0] - fixPoint[0]), 3), round((Circle['center'][1] - fixPoint[1]), 3))
        cv2.putText(chr_k, str(distance_to_fix[1]), (int(Circle['center'][0]), int(Circle['center'][1] / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(chr_k, str(distance_to_fix[0]), (int(Circle['center'][0] / 2), int(fixPoint[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        distances.append([distance_to_fix])
    cv2.imshow("CHR", chr_k)
    return distances, chr_k

jsn = Fast.readJson('Json/config.json')
imgPath = 'c:/Users/55419/Trabalho/Parallax/GitRepos/CEO96F/engine_H/Images/Lateral A.jpg'


Image = cv2.imread(imgPath)
Quadrants = Op.meshImg(Image)

Image = Quadrants[1][1]
cv2.imshow("Image", Image)
cv2.waitKey(0)
cv2.destroyWindow("Image")

def empty(a):
    a - a
    pass

cv2.namedWindow("Controle")
cv2.resizeWindow("Controle", 600, 600)
cv2.createTrackbar("H Min", "Controle", 0, 360, empty)
cv2.createTrackbar("H Max", "Controle", 360, 360, empty)
cv2.createTrackbar("S Min", "Controle", 0, 255, empty)
cv2.createTrackbar("S Max", "Controle", 255, 255, empty)
cv2.createTrackbar("V Min", "Controle", 0, 255, empty)
cv2.createTrackbar("V Max", "Controle", 255, 255, empty)
cv2.createTrackbar("A Min", "Controle", 0, 5000, empty)
cv2.createTrackbar("A Max", "Controle", 2000, 20000, empty)
cv2.createTrackbar("p", "Controle", 0, 10, empty)

cap = cv2.VideoCapture(0)
cap.set(3, 3264)
cap.set(4, 2448)
while cv2.waitKey(1) != 27:

    h_min = cv2.getTrackbarPos("H Min", "Controle")
    s_min = cv2.getTrackbarPos("S Min", "Controle")
    v_min = cv2.getTrackbarPos("V Min", "Controle")

    h_max = cv2.getTrackbarPos("H Max", "Controle")
    s_max = cv2.getTrackbarPos("S Max", "Controle")
    v_max = cv2.getTrackbarPos("V Max", "Controle")

    Amin = cv2.getTrackbarPos("A Min", "Controle")
    Amax = cv2.getTrackbarPos("A Max", "Controle")
    p = cv2.getTrackbarPos("p", "Controle")
    _, Image = cap.read()
    fixPoint = (int(Image.shape[1]/2), int(Image.shape[0]/2))
    Quadrants = Op.meshImg(Image)

    Image = Quadrants[1][1]
    _, img  =   findHole(Image, Amin, Amax, p, np.array([h_min, s_min, v_min]), np.array([h_max, s_max, v_max]))


print(f'"h_min":{h_min}, "s_min":{s_min}, "v_min":{v_min},')
print(f'"h_max":{h_max}, "s_min":{s_max}, "v_max":{v_max},')



