# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #
import FastFunctions as Ff
import OpencvPlus as Op
import numpy as np
import cv2

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

pFA = (50, 50)
pFB = (100, 60)
fixPoint = (pFB[0], int(pFA[1]+((pFB[1]-pFA[1])/2)))

Read = 'P_ (2).jpg' if not Hole else 'A2.jpg'
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


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #


def empty(a):
    pass
    return a


def finCircle(circle_Mask, areaMinC, areaMaxC, perimeter_size, blur_Size=3):
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


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Json-File                                                         #


HSVjsonIndex = 0
mainConfig = Ff.readJson('Json/config.json')
HSVjson = mainConfig['Filtros']['HSV']
HSValues = HSVjson[str(HSVjsonIndex)]['Valores']

HoleValues = mainConfig['Hole']

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


# Todo: Make a square around the cell.

Image = Quadrants[line][column]

for filterValues in HSValues:
    locals()[filterValues] = Op.extractHSValue(HSValues, filterValues)

for holeValue in HoleValues:
    locals()[holeValue] = HoleValues[holeValue]

largura2 = int(Image.shape[1])
altura2 = int(Image.shape[0])
edgeAnalyze = Image[0:altura2, 0:int(largura2 * bh)]


if DebugControls:
    cv2.namedWindow("Controls")
    cv2.resizeWindow("Controls", 600, 600)
    cv2.createTrackbar("H Min ", "Controls", lower[0], 255, empty)
    cv2.createTrackbar("S Min ", "Controls", lower[1], 255, empty)
    cv2.createTrackbar("V Min ", "Controls", lower[2], 255, empty)
    cv2.createTrackbar("H Max ", "Controls", upper[0], 255, empty)
    cv2.createTrackbar("S Max ", "Controls", upper[1], 255, empty)
    cv2.createTrackbar("V Max ", "Controls", upper[2], 255, empty)
    cv2.createTrackbar("X1 ", "Controls", areaMin, 40000, empty)
    cv2.createTrackbar("X2 ", "Controls", areaMax, 40000, empty)
    cv2.createTrackbar("X3 ", "Controls", perimeter, 10, empty)

    while True:
        h_min = cv2.getTrackbarPos("H Min ", "Controls")
        h_max = cv2.getTrackbarPos("H Max ", "Controls")
        s_min = cv2.getTrackbarPos("S Min ", "Controls")
        s_max = cv2.getTrackbarPos("S Max ", "Controls")
        v_min = cv2.getTrackbarPos("V Min ", "Controls")
        v_max = cv2.getTrackbarPos("V Max ", "Controls")
        X1 = cv2.getTrackbarPos("X1 ", "Controls")
        X2 = cv2.getTrackbarPos("X2 ", "Controls")
        X3 = cv2.getTrackbarPos("X3 ", "Controls")

        locals()['lower'] = np.array([h_min, s_min, v_min])
        locals()['upper'] = np.array([h_max, s_max, v_max])
        mask = Op.refineMask(Op.HSVMask(Image, lower, upper))
        chroma_key = cv2.bitwise_and(Image, Image, mask=mask)
        cv2.rectangle(chroma_key, pFA, pFB, (33, 48, 4), -1)
        cv2.drawMarker(chroma_key, fixPoint, (0, 255, 0), markerSize=10, thickness=1)
        if Hole:
            edgeInfo = finCircle(mask, X1, X2, X3)
            for Circle in edgeInfo:
                cv2.circle(chroma_key, (int(Circle['center'][0]), int(Circle['center'][1])), int(Circle['radius']),
                           (36, 255, 12), 2)
                cv2.line(chroma_key, (int(Circle['center'][0]), int(Circle['center'][1])), fixPoint, (168, 50, 131))
                cv2.line(chroma_key, (int(Circle['center'][0]), int(Circle['center'][1])),
                         (int(Circle['center'][0]), fixPoint[1]), (255, 0, 0))

                cv2.line(chroma_key, (int(Circle['center'][0]), fixPoint[1]), fixPoint, (0, 0, 255))
                distance = (Circle['center'][1] - fixPoint[1])
                cv2.putText(chroma_key, str(distance), (int(Circle['center'][0]), int(distance)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

        else:
            if Edge:
                mask = Op.refineMask(Op.HSVMask(edgeAnalyze, lower, upper))
                cv2.rectangle(mask, (0, 0), (mask.shape[1], mask.shape[0]), (0, 0, 0), thickness=20)
                chroma_key = cv2.bitwise_and(edgeAnalyze, edgeAnalyze, mask=mask)
                Contorno, Null = Op.findContoursPlus(mask, AreaMin_A=X1, AreaMax_A=X2)
                for info in Contorno:
                    cv2.drawContours(chroma_key, [info['contour']], -1, (70, 20, 20), 3)
                    cv2.drawMarker(chroma_key, tuple(info['contour'][0]), (20, 20, 70), markerSize=10, thickness=3)
                    cv2.drawMarker(chroma_key, tuple(info['contour'][3]), (20, 20, 70), markerSize=10, thickness=3)
                    PL = tuple(info['contour'][0])
                    PL1 = (int(largura2), int(info['contour'][0][1]))
                    Edge = False
                cv2.imshow('edgeAnalyze', cv2.resize(edgeAnalyze, None, fx=Escala, fy=Escala))
            else:
                cv2.line(chroma_key, PL, PL1, (0, 255, 0), 10)
                edgeAnalyze = Image[PL[1]: altura2, 0:largura2]
                mask = Op.refineMask(Op.HSVMask(edgeAnalyze, lower, upper))
                cv2.rectangle(mask, (0, 0), (mask.shape[1], mask.shape[0]), (0, 0, 0), thickness=20)
                chroma_key = cv2.bitwise_and(edgeAnalyze, edgeAnalyze, mask=mask)
                Contorno, Null = Op.findContoursPlus(mask, AreaMin_A=X1, AreaMax_A=X2)
                for info in Contorno:
                    cv2.drawContours(chroma_key, [info['contour']], -1, (70, 20, 20), 3)
                    cv2.drawMarker(chroma_key, tuple(info['contour'][0]), (20, 20, 70), markerSize=10, thickness=3)
                    cv2.drawMarker(chroma_key, tuple(info['contour'][3]), (20, 20, 70), markerSize=10, thickness=3)

        cv2.imshow('Chroma Key', cv2.resize(chroma_key, None, fx=Escala, fy=Escala))
        cv2.imshow('Mask', cv2.resize(mask, None, fx=Escala, fy=Escala))
        Key = cv2.waitKey(1)
        if Key == 27:
            cv2.destroyAllWindows()
            print(lower, upper)
            break
else:
    Tabs = [mainConfig['Edge'], mainConfig['Screw']]

    mask = Op.refineMask(Op.HSVMask(Image, lower, upper))
    chroma_key = cv2.bitwise_and(Image, Image, mask=mask)
    cv2.rectangle(chroma_key, pFA, pFB, (33, 48, 4), -1)
    cv2.drawMarker(chroma_key, fixPoint, (0, 255, 0), markerSize=10, thickness=1)

    if Hole:
        for filterValues in HSValues:
            locals()[filterValues] = np.array(Op.extractHSValue(HSValues, filterValues))

        edgeInfo = finCircle(mask, areaMin, areaMax, perimeter)
        for Circle in edgeInfo:
            cv2.circle(chroma_key, (int(Circle['center'][0]), int(Circle['center'][1])), int(Circle['radius']),
                       (36, 255, 12), 2)

            cv2.line(chroma_key, (int(Circle['center'][0]), int(Circle['center'][1])), fixPoint, (168, 50, 131))

            cv2.line(chroma_key, (int(Circle['center'][0]), int(Circle['center'][1])),
                     (int(Circle['center'][0]), fixPoint[1]), (255, 0, 0))

            cv2.line(chroma_key, (int(Circle['center'][0]), fixPoint[1]), fixPoint, (0, 0, 255), thickness=2)

            distance = (round((Circle['center'][0]-fixPoint[0]), 3), round((Circle['center'][1] - fixPoint[1]), 3))
            cv2.putText(chroma_key, str(distance[1]), (int(Circle['center'][0]), int(Circle['center'][1]/2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            cv2.putText(chroma_key, str(distance[0]), (int(Circle['center'][0]/2), int(fixPoint[1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else:
        for Tab in range(len(Tabs)):
            for filterValues in HSVjson[str(Tab + 1)]['Valores']:
                locals()[filterValues] = Op.extractHSValue(HSVjson[str(Tab + 1)]['Valores'], filterValues)
            mask = Op.refineMask(Op.HSVMask(edgeAnalyze, lower, upper))
            cv2.rectangle(mask, (0, 0), (mask.shape[1], mask.shape[0]), (0, 0, 0), thickness=20)
            chroma_key = cv2.bitwise_and(edgeAnalyze, edgeAnalyze, mask=mask)
            Contorno, Null = Op.findContoursPlus(mask, AreaMin_A=Tabs[Tab]['areaMin'], AreaMax_A=Tabs[Tab]['areaMax'])
            for info in Contorno:
                cv2.drawContours(chroma_key, [info['contour']], -1, (70, 20, 20), 3)
                cv2.drawMarker(chroma_key, tuple(info['contour'][0]), (20, 20, 70), markerSize=10, thickness=3)
                cv2.drawMarker(chroma_key, tuple(info['contour'][3]), (20, 20, 70), markerSize=10, thickness=3)
                if Tab == 0:
                    PL = tuple(info['contour'][0])
                    PL1 = (int(largura2), int(info['contour'][0][1]))
                    edgeAnalyze = Image[PL[1]: altura2, 0:largura2]
                    pass
                if Tab == 1:
                    cv2.line(chroma_key, tuple(info['contour'][0]), tuple(info['contour'][1]),
                             (0, 255, 255), thickness=3)
                    distance = info['contour'][0][1] - info['contour'][1][1]
                    cv2.putText(chroma_key, str(distance), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), thickness=3)
    print(distance)
    cv2.imshow('Chroma Key', cv2.resize(chroma_key, None, fx=Escala, fy=Escala))
    cv2.imshow('Image', cv2.resize(Image, None, fx=Escala, fy=Escala))
    cv2.waitKey(0)
