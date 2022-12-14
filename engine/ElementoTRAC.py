# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #


def Ajusta(x):
    return round((0.0059*(x**2)) + (0.2741*x) + (0.6205), 2)


def Parafusa(pos, voltas=2, mm=0, servo=0, angulo=0):
        Fast.M400(arduino)
        Fast.sendGCODE(arduino, f'g91')
        Fast.sendGCODE(arduino, f'g38.3 z-{pos} F{zMaxFed}')
        Fast.sendGCODE(arduino, f'g0 z-{mm} {zMaxFed}')
        Fast.sendGCODE(arduino, f'm280 p{servo} s{angulo}')
        Fast.sendGCODE(arduino, f'm43 t s10 l10 w{voltas*50}')
        Fast.sendGCODE(arduino, 'g90')
        Fast.sendGCODE(arduino, f'g0 z{pos} F{2000}')
        Fast.M400(arduino)

import FastFunctions as Fast
import OpencvPlus as Op
import operator as opr
import numpy as np
import timeit
from  random import randint
import time
import cv2
T0A = timeit.default_timer()


Cortes = Fast.readJson("../engine/Json/HolePoints.json")

_, code, arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Variables                                                         #
perimeter = [None]
areaMin = [None]
areaMax = [None]
lower = [None]
upper = [None]
distance = True
Hole = True
Edge = True

cap = cv2.VideoCapture(1)
cap.set(3, 3264)
cap.set(4, 2448)

# cap1 = cv2.VideoCapture(0)
# cap1.set(3, 3264)
# cap1.set(4, 2448)

Read = 'Lateral B.jpg' if not Hole else 'Lateral A.jpg'
pathImages = 'c:/Users/55419/Trabalho/Parallax/GitRepos/CEO96F/engine/Images/'

markerOffset = 5
PL = PL1 = 0
bh = 0.3

Image = cv2.imread(pathImages + Read)
Escala = 0.45
divided = 3

# Quadrants = Op.meshImg(Image)
# largura = int(Image.shape[1])
# altura = int(Image.shape[0])
# pFB = (100, 60)
# pFA = (50, 50)
#fixPoint = (pFB[0], int(pFA[1]+((pFB[1]-pFA[1])/2)))


column = 1
line = 1
raio = 60

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #


def empty(a):
    pass
    return a


def findCircle(circle_Mask, areaMinC, areaMaxC, perimeter_size, blur_Size=3):
    global raio
    circle_info = []
    blur = cv2.medianBlur(circle_Mask, blur_Size)
    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    cv2.imshow("Open", cv2.resize(
                opening, None, fx=Escala, fy=Escala/2))
    #mask = cv2.erode(mask, kernel, iterations=6)

    edges = cv2.findContours(
        opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edges = edges[0] if len(edges) == 2 else edges[1]
    ids = 0
    for c in edges:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(c)
        if len(approx) >= perimeter_size and areaMinC < area < areaMaxC:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if r >= 50 and r<=80:
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
    for aba in range(len(tabs)):
        for value in HSVjson[str(aba)]['Valores']:
            globals()[value] = Op.extractHSValue(
                HSVjson[str(aba + 1)]['Valores'], value)
        msk = Op.refineMask(Op.HSVMask(edge_analyze, lower, upper))
        cv2.rectangle(
            msk, (0, 0), (msk.shape[1], msk.shape[0]), (0, 0, 0), thickness=20)
        chr_k = cv2.bitwise_and(edge_analyze, edge_analyze, mask=msk)
        edge, null = Op.findContoursPlus(
            msk, AreaMin_A=tabs[aba]['areaMin'], AreaMax_A=tabs[aba]['areaMax'])
        if edge:
            for info_edge in edge:
                cv2.drawContours(
                    chr_k, [info_edge['contour']], -1, (70, 255, 20), 3)
                if aba == 0:
                    point_a = tuple(info_edge['contour'][0])
                    edge_analyze = imgAnalyse[point_a[1]: height, 0:width]
                    pass
                if aba == 1:
                    offset_screw = round(info_edge['dimension'][0], 3)
                    cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), thickness=3)
        else:
            return offset_screw, chr_k
    return offset_screw, chr_k


def findHole(imgAnalyse, minArea, maxArea, c_perimeter, HSValues, fixed_Point, escala_real=5):
    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    for filter_values in HSValues:
        locals()[filter_values] = np.array(
            Op.extractHSValue(HSValues, filter_values))
    
    mask = Op.refineMask(Op.HSVMask(imgAnalyse, locals()
                         ['lower'], locals()['upper']))
    chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
    distances = []
    edge = findCircle(mask, minArea, maxArea, c_perimeter)
    for Circle in edge:
        cv2.circle(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), int(Circle['radius']),
                   (36, 255, 12), 2)

        cv2.line(chr_k, (int(Circle['center'][0]), int(
            Circle['center'][1])), fixed_Point, (168, 50, 131))

        cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])),
                 (int(Circle['center'][0]), fixed_Point[1]), (255, 0, 0))

        cv2.line(chr_k, (int(Circle['center'][0]), fixed_Point[1]),
                 fixed_Point, (0, 0, 255), thickness=2)

        distance_to_fix = (round((Circle['center'][0] - fixed_Point[0])*(escala_real/(Circle['radius']*2)), 2),
                           round((Circle['center'][1] - fixed_Point[1])*(escala_real/(Circle['radius']*2)), 2))
        cv2.putText(chr_k, str(distance_to_fix[1]), (int(Circle['center'][0]), int(Circle['center'][1] / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(chr_k, str(distance_to_fix[0]), (int(Circle['center'][0] / 2), int(fixed_Point[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.putText(chr_k, str(Circle["id"]), (int(Circle["center"][0]), int(Circle["center"][1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
        distances.append(distance_to_fix)
    return distances, chr_k, (Circle['radius']*2)
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

machineConfig = Fast.readJson('Json/machine.json')
feedRatePercent = 50/100
xMaxFed = int(machineConfig["configuration"]["informations"]["machine"]["maxFeedrate"]["xMax"])*feedRatePercent
yMaxFed = int(machineConfig["configuration"]["informations"]["machine"]["maxFeedrate"]["yMax"])*0.7
zMaxFed = int(machineConfig["configuration"]["informations"]["machine"]["maxFeedrate"]["zMax"])
eMaxFed = int(machineConfig["configuration"]["informations"]["machine"]["maxFeedrate"]["aMax"])*feedRatePercent
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Code-Exec                                                         #


def Setup_local():
    for holeValue in HoleValues:
        globals()[holeValue] = HoleValues[holeValue]

Setup_local()


while cv2.waitKey(1) != 27:
    img = img = cv2.imread("../engine/Images/0.jpg")
    img_draw = img.copy()

    precicao = 0.4
    dsts = 0
    Pos = []
    for lados in range(4):
        tentavias = 0
        while tentavias<=3:
            for Pontos in Cortes:
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
                #            Corta a imagem e faz as marca????es               #

                show = img[Pontos["P0"][1]:Pontos["P0"][1] + Pontos["P1"][1],
                        Pontos["P0"][0]:Pontos["P0"][0] + Pontos["P1"][0]]
                pa, pb = tuple(Pontos["P0"]),(Pontos["P0"][0]+Pontos["P1"][0],
                                              Pontos["P0"][1]+Pontos["P1"][1])

                cv2.drawMarker(img_draw, pa, (255, 50, 0), thickness=10)
                cv2.drawMarker(img_draw, pb, (50, 255, 0), thickness=10)
                cv2.rectangle(img_draw, pa, pb, (255, 50, 255), 10)

                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
                #                      Procura os furos                      #

                Resultados, R, per = findHole(show, areaMin, areaMax, perimeter, HSValues, (int((pb[0]-pa[0])/2),int((pb[1]-pa[1])/2)))

                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
                #                           X-ray                            #

                img_draw[Pontos["P0"][1]:Pontos["P0"][1] + show.shape[0],
                        Pontos["P0"][0]:Pontos["P0"][0] + show.shape[1]] = R

                cv2.drawMarker(img_draw, (int((pa[0]+pb[0])/2),
                                          int((pa[1]+pb[1])/2)),
                                          (255,0,0),
                                          thickness=5,
                                          markerSize=50)

                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
                #                          Exibe                             #
                cv2.imshow("show", cv2.resize(show, None, fx=0.25, fy=0.25))
                cv2.imshow("draw", cv2.resize(img_draw, None, fx=0.25, fy=0.25))
                cv2.waitKey(1)

                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
                #                     Verifica a dist??ncia                   #
                if Resultados:
                    MY = Resultados[dsts][0]
                    MX = Resultados[dsts][1]
                    MX += (randint(-int(abs(MX)/4),abs(int(MX))))
                    if abs(MX) > precicao:
                        #Fast.sendGCODE(arduino, f"G0 X{MX} Y0 F{xMaxFed}", echo=True)
                        print(f"G0 X{MX} Y0 F{xMaxFed}")
                        
                    elif abs(MY) > precicao:
                        aMY = Ajusta(abs(MY))
                        aMY *= -1 if MY < 0 else 1
                        # Fast.sendGCODE(arduino, f"G0 X0 Y{aMY} F{yMaxFed}", echo=True)
                        print(f"G0 X0 Y{aMY} F{yMaxFed}")

                    # Fast.sendGCODE(arduino, f"G4 S0.3", echo=True)
                    time.sleep(0.5)
                    #Fast.M400(arduino)
                    tentavias+=1
                    print("Tentativa:", tentavias)
                    if abs(MY) <= precicao and abs(MX) <= precicao:
                        Pos.append(Fast.M114(arduino))
                        if len(Resultados)>1:
                            if dsts == 0:
                                dsts += 1
                            else:
                                tentavias = 10
                        else:
                            tentavias = 10
        print("Passando pro lado:", lados+1)
    break      

print(Pos)





exit()
Fast.sendGCODE(arduino, "G28 Y")
Fast.sendGCODE(arduino, "G28 X Z")
Parafusa(140, mm=5, voltas=20)
Fast.sendGCODE(arduino, f"G0 X5 F{xMaxFed}")
Fast.sendGCODE(arduino, f"G0 Y49 F{yMaxFed}")
Fast.M400(arduino)
Fast.sendGCODE(arduino, "M42 P31 S255")
Fast.sendGCODE(arduino, "G4 S1")
Fast.sendGCODE(arduino, "G28 Y")
Fast.sendGCODE(arduino, f"G0 X80 F{xMaxFed}")
Fast.sendGCODE(arduino, f"G0 Y9 F{yMaxFed}")
Fast.M400(arduino)
Fast.sendGCODE(arduino, "M42 P32 S255")
Fast.sendGCODE(arduino, "G91")
for x in range(20):
    _, Image = cap.read()
    time.sleep(0.3)

p1 = tuple(map(opr.add, map(opr.mul, (((Quadrants[line][column]).shape[:2])[
           ::-1]), (column, line)), (250, -550)))
p2 = tuple(map(opr.add, map(opr.mul, ((
    (Quadrants[line-1][column-1]).shape[:2])[::-1]), (column+1, line+1)), (-250, 550)))
cv2.rectangle(Image, p1, p2, (0, 0, 255), 5)


cv2.imshow('Image_Original', cv2.resize(
                Image, None, fx=Escala*0.3, fy=Escala*0.3))
cv2.waitKey(0)
Image = Image[p1[1]:p2[1], p1[0]:p2[0]]
fixPoint = (int(Image.shape[1]/2), int(Image.shape[0]/2))

for holeValue in HoleValues:
    locals()[holeValue] = HoleValues[holeValue]

Tabs = [mainConfig['Mask_Parameters']['Edge'],
        mainConfig['Mask_Parameters']['Screw']]

T0A = timeit.default_timer()
Etapa = 0
if Etapa ==0:
    tag = 0
    precicao = 0.4
    Pos = []
    T0 = timeit.default_timer()
    for z in range(4):
        MY = 1
        MX = 1
        MMY = 0
        x = 0
        dsts = 0
        tag = randint(tag,tag+101)
        while True:
            try:
                _, Image = cap.read()
                p1 = tuple(map(opr.add, map(opr.mul, (((Quadrants[line][column]).shape[:2])[
                        ::-1]), (column, line)), (240, -550)))
                p2 = tuple(map(opr.add, map(opr.mul, ((
                    (Quadrants[line-1][column-1]).shape[:2])[::-1]), (column+1, line+1)), (-240, 550)))
                cv2.rectangle(Image, p1, p2, (0, 0, 255), 5)
                cv2.imshow('Image_Original', cv2.resize(
                    Image, None, fx=Escala, fy=Escala/2))
                cv2.waitKey(1)
                Image = Image[p1[1]:p2[1], p1[0]:p2[0]]
                Resultados, R, per = findHole(Image, areaMin, areaMax, perimeter,HSValues, fixPoint)
                cv2.drawMarker(R, fixPoint, (255,0,0),thickness=5, markerSize=50)
                cv2.imshow("Imagem",  cv2.resize(
                    R, None, fx=Escala, fy=Escala/2))
                    # , findScrew(Image, Tabs)]
                if Resultados:
                    MY = Resultados[dsts][0]
                    MX = Resultados[dsts][1]
                    if abs(MX) > precicao:
                        Fast.sendGCODE(arduino, f"G0 X{MX} Y0 F{xMaxFed}", echo=True)
                        
                    elif abs(MY) > precicao:
                        aMY = Ajusta(abs(MY))
                        aMY *= -1 if MY < 0 else 1
                        Fast.sendGCODE(arduino, f"G0 X0 Y{aMY} F{yMaxFed}", echo=True)
                    Fast.sendGCODE(arduino, f"G4 S0.3", echo=True)
                    time.sleep(0.5)
                    x += 1
                    MMY += abs(MY)
                    if abs(MY) <= precicao and abs(MX) <= precicao:
                        cv2.imwrite(f"./Images/AutoAjuste{x}_{dsts}_{tag}.jpg", R)
                        Pos.append(Fast.M114(arduino))
                        if len(Resultados)>1:
                            if dsts == 0:
                                dsts += 1
                            else:
                                break
                        else:
                            break
            except Exception as ex:
                print(Pos)
                print(ex)
                pass
        print(Fast.sendGCODE(arduino, f"G0 e -90 F{eMaxFed}", echo=True))
        time.sleep(2)
        cv2.destroyAllWindows
    Fast.sendGCODE(arduino, "M42 P32 S0")
    Fast.sendGCODE(arduino, "M42 P33 S255")
    print("Tempo de Execu????o:", round(timeit.default_timer()-T0A, 3))

    Cam = {'X':74.5, 'Y':7.5}
    FuraPos = {'X':240, 'Y':16}
    CamDiff = {'X':FuraPos['X']-Cam['X'], 'Y':FuraPos['Y']-Cam['Y']}
    PosFinal =[]
    for poss in Pos:
        print(-round(Cam['X']-poss['X'], 2), CamDiff['X'])
        PosFinal.append({'X':-round(Cam['X']-poss['X'], 2)+FuraPos['X'], 'Y':-round(Cam['Y']-poss['Y'], 2)+FuraPos['Y'], 'E':poss['E']} )

    Fast.sendGCODE(arduino, 'g90')
    print("Tempo final:", timeit.default_timer() - T0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    for poss in PosFinal:
        Fast.sendGCODE(arduino, f"g0 X{poss['X']} E{poss['E']} F{xMaxFed}")
        Fast.sendGCODE(arduino, f"g0 Y{poss['Y']} F{yMaxFed}")
        Parafusa(140, mm=0, voltas=20)
        Fast.sendGCODE(arduino, f"g0 X{100} F{xMaxFed}")
        Parafusa(140, mm=0, voltas=20)

cap.release()
Fast.sendGCODE(arduino, "M42 P33 S255")
# cap1.release()