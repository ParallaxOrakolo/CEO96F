# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #
import FastFunctions as Fast
import OpencvPlus as Op
import operator as opr
import numpy as np
import timeit
import time
import cv2
T0A = timeit.default_timer()
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Variables                                                         #
perimeter = [None]
areaMin = [None]
areaMax = [None]
lower = [None]
upper = [None]

distance = True
Hole = False
Edge = True

cap = cv2.VideoCapture(0)
cap.set(3, 3264)
cap.set(4, 2448)

# pFB = (100, 60)
# pFA = (50, 50)
# fixPoint = (pFB[0], int(pFA[1]+((pFB[1]-pFA[1])/2)))

Read = '\Lateral A.jpg' if not Hole else '\Lateral A.jpg'
pathImages = ".\Images"

markerOffset = 5
PL = PL1 = 0
bh = 0.3

Image = cv2.imread(pathImages + Read)
Escala = 0.45
divided = 3
Quadrants = Op.meshImg(Image)
largura = int(Image.shape[1])
altura = int(Image.shape[0])

column = 1
line = 1


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #


def empty(a):
    pass
    return a


def findCircle(circle_Mask, areaMinC, areaMaxC, perimeter_size, blur_Size=3):
    circle_info = []
    blur = cv2.medianBlur(circle_Mask, blur_Size)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    edges = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edges = edges[0] if len(edges) == 2 else edges[1]
    ids = 0
    for c in edges:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(c)
        if len(approx) > perimeter_size and areaMinC < area < areaMaxC:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            circle_info.append({"center": (x, y), "radius": r, "id": ids})
            ids += 1
    return circle_info


def findScrew(imgAnalyse, tabs):

    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    width = int(Image.shape[1])
    height = int(Image.shape[0])
    offset_screw = 0.00
    edge_analyze = imgAnalyse[0:height, 0:int(width * bh)]
    chr_k = imgAnalyse
    for aba in tabs:
        for value in HSVjson[aba]['Valores']:
            globals()[value] = Op.extractHSValue(HSVjson[aba]['Valores'], value)
        msk = Op.refineMask(Op.HSVMask(edge_analyze, lower, upper))
        cv2.rectangle(msk, (0, 0), (msk.shape[1], msk.shape[0]), (0, 0, 0), thickness=20)
        chr_k = cv2.bitwise_and(edge_analyze, edge_analyze, mask=msk)
        edge, null = Op.findContoursPlus(msk, AreaMin_A=mainConfig['Mask_Parameters'][aba]['areaMin'], AreaMax_A=mainConfig['Mask_Parameters'][aba]['areaMax'])
        if edge:
            for info_edge in edge:
                cv2.drawContours(chr_k, [info_edge['contour']], -1, (70, 255, 20), 3)
                if aba == "Edge":
                    point_a = tuple(info_edge['contour'][0])
                    edge_analyze = imgAnalyse[point_a[1]: height, 0:width]
                    pass
                if aba == "Screw":
                    offset_screw = round(info_edge['dimension'][0], 3)
                    cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), thickness=3)
        else:
            return offset_screw, chr_k
    return offset_screw, chr_k


def findHole(imgAnalyse, minArea, maxArea, c_perimeter):

    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    for values in HSValues:
        globals()[values] = np.array(Op.extractHSValue(HSValues, values))

    mask = Op.refineMask(Op.HSVMask(imgAnalyse, lower, upper))
    cv2.imshow("Mask", mask)
    chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
    cv2.imshow("CHR", chr_k)
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
        
        cv2.putText(chr_k, str(Circle["id"]), (int(Circle["center"][0]), int(Circle["center"][1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

        distances.append(distance_to_fix)
    return distances, chr_k
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Json-File                                                         #


HSVjsonIndex = 0
mainConfig = Fast.readJson('Json/config.json')
HSVjson = mainConfig['Filtros']['HSV']
HSValues = HSVjson['Hole']['Valores']

HoleValues = mainConfig['Mask_Parameters']['Hole']

DebugTypes = mainConfig['Debugs']
if DebugTypes["all"]:
    DebugPrint = DebugPictures = DebugRT = DebugMarkings = True
    DebugControls = False
else:
    DebugPrint = DebugTypes["print"]
    DebugPictures = DebugTypes["pictures"]
    DebugRT = DebugTypes["realTime"]
    DebugMarkings = DebugTypes["markings"]
    DebugControls = DebugTypes["testControls"]


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Code-Exec                                                         #

arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')

print(Fast.sendGCODE(arduino, "G28 Y", echo=True))
print(Fast.sendGCODE(arduino, "G28 X", echo=True))
print(Fast.sendGCODE(arduino, "G0 X33", echo=True))
print(Fast.sendGCODE(arduino, "G0 Y45", echo=True))
print(Fast.sendGCODE(arduino, "M42 I P31 S255", echo=True))
print(Fast.sendGCODE(arduino, "G28 Y", echo=True))
print(Fast.sendGCODE(arduino, "G0 X97", echo=True))
print(Fast.sendGCODE(arduino, "G0 Y5 ", echo=True))
print(Fast.sendGCODE(arduino, "G91", echo=True))



# Make a square around the cell.
p1 = tuple(map(opr.add, map(opr.mul, (((Quadrants[line][column]).shape[:2])[::-1]), (column, line)), (-10, -10)))
p2 = tuple(map(opr.add, map(opr.mul, (((Quadrants[line-1][column-1]).shape[:2])[::-1]), (column+1, line+1)), (10, 10)))
cv2.rectangle(Image, p1, p2, (0, 0, 255), 5)

#cv2.imshow('Image_Original', cv2.resize(Image, None, fx=Escala*0.3, fy=Escala*0.3))

Image = Quadrants[line][column]
fixPoint = (int(Image.shape[1]/2), int(Image.shape[0]/2))

for filterValues in HSValues:
    locals()[filterValues] = Op.extractHSValue(HSValues, filterValues)

for holeValue in HoleValues:
    locals()[holeValue] = HoleValues[holeValue]

Tabs = ['Edge','Screw']

T0A = timeit.default_timer()
for z in range(3):
    MY = 0.4
    MX = 0.4
    MMY = 0
    x = 0
    while abs(MY) > 0.1 or abs(MX) > 0.1:
    # for zz in range(5):
        try:
            _, Image = cap.read()
            Quadrants = Op.meshImg(Image)
            p1 = tuple(map(opr.add, map(opr.mul, (((Quadrants[line][column]).shape[:2])[::-1]), (column, line)), (-10, -10)))
            p2 = tuple(map(opr.add, map(opr.mul, (((Quadrants[line-1][column-1]).shape[:2])[::-1]), (column+1, line+1)), (10, 10)))
            cv2.rectangle(Image, p1, p2, (0, 0, 255), 5)
            cv2.imshow('Image_Original', cv2.resize(Image, None, fx=Escala*0.3, fy=Escala*0.3))
            cv2.waitKey(1)
            Image = Quadrants[line][column]
            Resultados = [findHole(Image, areaMin, areaMax, perimeter), findScrew(Image, Tabs)]
            R = Resultados[0][1]
            if Resultados[0][0]:
                print("Distancias:", Resultados[0][0])
                MY = round((0.5/raio)*Resultados[0][0][0][0][0], 2)
                MX = round((0.5/raio)*Resultados[0][0][0][0][1], 2)
                print("dst Y:", MY)
                print("dst X:", MX)   
                cv2.imshow("Imagem", Resultados[0][1])
                #cv2.waitKey(200)
                #cv2.imwrite(f"AutoAjuste{x}.jpg", Resultados[0][1] )
                Fast.sendGCODE(arduino, f"G0 X{MX} Y{MY} F500", echo=True)
                x+=1
                MMY += abs(MY)
        except Exception as ex:
            print(ex)
            pass
    print(Fast.sendGCODE(arduino, "G0 e -90 F5000", echo=True))
    time.sleep(2)
    cv2.destroyAllWindows
print(Fast.sendGCODE(arduino, "G0 e -90 F5000", echo=True))
print("Tempo de Execução:", round(timeit.default_timer()-T0A, 3))
print("Movimentos:", MMY)

# Resultados = [findHole(Image, areaMin, areaMax, perimeter), findScrew(Image, Tabs)]
# cv2.imshow("Imagem", Resultados[1][1])
# cv2.waitKey(0)
# print("Tempo de Execução:", round(timeit.default_timer()-T0A, 3))
