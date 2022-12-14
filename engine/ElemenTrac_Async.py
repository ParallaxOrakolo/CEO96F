# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #
import FastFunctions as Ff
import OpencvPlus as Op
import operator as opr
import numpy as np
import asyncio
import timeit
from random import randint
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
Hole = True
Edge = True

pFB = (100, 60)
pFA = (50, 50)
fixPoint = (pFB[0], int(pFA[1] + ((pFB[1] - pFA[1]) / 2)))

Read = 'P_ (3).jpg' if not Hole else 'A3.jpg'
pathImages = 'Images/'

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

show_resize = 0.5
show_time = 5
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #


def empty(a):
    pass
    return a


async def findCircle(circle_Mask, areaMinC, areaMaxC, perimeter_size, blur_Size=3):
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
    await asyncio.sleep(0.0)
    return circle_info


async def findScrew(event2, event3, show, imgAnalyse, tabs):
    await asyncio.sleep(0.0)
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
            globals()[value] = Op.extractHSValue(HSVjson[str(aba + 1)]['Valores'], value)
        msk = Op.refineMask(Op.HSVMask(edge_analyze, lower, upper))
        cv2.rectangle(msk, (0, 0), (msk.shape[1], msk.shape[0]), (0, 0, 0), thickness=20)
        chr_k = cv2.bitwise_and(edge_analyze, edge_analyze, mask=msk)
        edge, null = Op.findContoursPlus(msk, AreaMin_A=tabs[aba]['areaMin'], AreaMax_A=tabs[aba]['areaMax'])
        if edge:
            for info_edge in edge:
                cv2.drawContours(chr_k, [info_edge['contour']], -1, (70, 255, 20), 3)
                if aba == 0:
                    point_a = tuple(info_edge['contour'][0])
                    edge_analyze = imgAnalyse[point_a[1]: height, 0:width]
                    pass
                if aba == 1:
                    offset_screw = round(info_edge['dimension'][0], 3)
                    cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), thickness=3)
        else:
            if show:
                asyncio.create_task(ShowImage('Screw', chr_k, show_resize, show_time, asyncio.Event()))
            else:
                event2.set()
            return offset_screw, chr_k
    if show:
        asyncio.create_task(ShowImage('Screw', chr_k, show_resize, show_time, asyncio.Event()))
    else:
        event2.set()

    # while not event3.is_set():
    #     pass
    return offset_screw, chr_k


async def findHole(event2, event3, show, imgAnalyse, minArea, maxArea, c_perimeter):
    await asyncio.sleep(0.0)
    global img
    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    for values in HSValues:
        globals()[values] = np.array(Op.extractHSValue(HSValues, values))

    mask = Op.refineMask(Op.HSVMask(imgAnalyse, lower, upper))
    chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
    distances = []
    edge = await asyncio.create_task(findCircle(mask, minArea, maxArea, c_perimeter))
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
        distances.append([distance_to_fix, 'id:', randint(250, 500)])
    if show:
        asyncio.create_task(ShowImage('Hole', chr_k, show_resize, show_time, event2))
    else:
        event2.set()

    while not event3.is_set():
        print("Preso")
        await asyncio.sleep(0.3)
    print("Soltou")
    return distances, chr_k


async def CloseProcess(event, event2):
    while not event.is_set():
        if event2.is_set():
            event.set()
        await asyncio.sleep(0.0)


async def ShowImage(name, img, resize, time, close_event, debug=False, permanent=False):
    close_event.clear()
    if debug:
        print("ShowImage")
    if permanent:
        while not close_event.is_set():
            cv2.imshow(str(name), cv2.resize(img, None, fx=resize, fy=resize))
            await asyncio.sleep(0.0)
    else:
        # cv2.imshow(str(name), cv2.resize(img, None, fx=resize, fy=resize))
        cv2.imshow(str(name), cv2.resize(img, None, fx=resize, fy=resize))
        cv2.waitKey(1)
        await asyncio.sleep(time)
        close_event.set()


async def Main():
    event = asyncio.Event()
    event2 = asyncio.Event()
    event3 = asyncio.Event()
    nada = asyncio.create_task(CloseProcess(event, event2))
    hct = timeit.default_timer()
    RESERVA_resultado = asyncio.gather(*[findHole(event2, event3, True, Image, areaMin, areaMax, perimeter),
                                         findScrew(event2, event3, True, Image, Tabs)])
    print("Cria????o a Thread", round(timeit.default_timer()-hct, 5))
    event3.set()
    hcd = timeit.default_timer()
    resultado = await RESERVA_resultado
    if resultado:
        print("Valida????o de dados:", round(timeit.default_timer()-hcd, 5))
    nada = await nada
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Json-File                                                         #


HSVjsonIndex = 0
mainConfig = Ff.readJson('Json/config.json')
HSVjson = mainConfig['Filtros']['HSV']
HSValues = HSVjson[str(HSVjsonIndex)]['Valores']

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
#                                              Variables - with json                                                   #

arduino = Ff.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')

# Make a square around the cell.
p1 = tuple(map(opr.add, map(opr.mul, (((Quadrants[line][column]).shape[:2])[::-1]), (column, line)), (-10, -10)))
p2 = tuple(
    map(opr.add, map(opr.mul, (((Quadrants[line - 1][column - 1]).shape[:2])[::-1]), (column + 1, line + 1)), (10, 10)))
cv2.rectangle(Image, p1, p2, (0, 0, 255), 5)
cv2.imshow('Image_Original', cv2.resize(Image, None, fx=Escala * 0.35, fy=Escala * 0.35))
cv2.waitKey(0)
Image = Quadrants[line][column]

for filterValues in HSValues:
    locals()[filterValues] = Op.extractHSValue(HSValues, filterValues)

for holeValue in HoleValues:
    locals()[holeValue] = HoleValues[holeValue]

Tabs = [mainConfig['Mask_Parameters']['Edge'], mainConfig['Mask_Parameters']['Screw']]


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Code-Exec                                                         #

asyncio.run(Main())

print("Tempo de Execu????o:", round(timeit.default_timer() - T0A, 3))




