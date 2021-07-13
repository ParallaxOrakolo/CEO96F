import cv2
import numpy as np
import operator as opr
import FastFunctions as Fast
import OpencvPlus as Op

column = 1
line = 2
bh = 0.3
def empty(a):
    a-a
    pass


def findScrew(imgAnalyse, FiltrosHSV, MainJson, processos, bh=0.3, **kwargs):

    force = kwargs.get('aba', False)
    edge_only = kwargs.get('edge_only', False)
    confs = kwargs.get('manual', False)
    trav = False
    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    width = int(imgAnalyse.shape[1])
    height = int(imgAnalyse.shape[0])
    offset_screw = 0.00
    if isinstance(edge_only, tuple):
        edge_analyze = imgAnalyse[edge_only[0]+10:edge_only[1], edge_only[2]+400:edge_only[3]-150]
    else:    
        edge_analyze = imgAnalyse[0:int(height), (int(width/2)-100):(int(width/2)+100)]
    chr_k = imgAnalyse
    tabs = []
    for indexes in FiltrosHSV:
        if FiltrosHSV[indexes]["Application"] in processos:
            tabs.append((
                FiltrosHSV[indexes]["Application"],
                list(FiltrosHSV[indexes]['Valores'].keys()),
                FiltrosHSV[indexes]['Valores']
            ))
    for aba, keys, value in tabs:
        if not trav:
            for key in keys:
                locals()[key] = Op.extractHSValue(value, key)
        if type(force) == int:
            trav = True
        
        if not confs:
            l, u = locals()['lower'], locals()['upper']
            a, A = MainJson['Mask_Parameters'][aba]['areaMin'], MainJson['Mask_Parameters'][aba]['areaMax']
        else:
            l, u = np.array([h_min, s_min, v_min]), np.array([h_max, s_max, v_max])
            a, A = Amin, Amax
        msk = Op.refineMask(Op.HSVMask(
            #edge_analyze, np.array([h_min, s_min, v_min]), np.array([h_max, s_max, v_max])))
            edge_analyze, l, u))
        cv2.rectangle(
            msk, (0, 0), (msk.shape[1], msk.shape[0]), (0, 0, 0), thickness=20)
        chr_k = cv2.bitwise_and(edge_analyze, edge_analyze, mask=msk)
        edge, _ = Op.findContoursPlus(msk,
                                     AreaMin_A=a,
                                     AreaMax_A=A
                                    #   AreaMin_A=Amin,
                                    #   AreaMax_A=Amax
                                      )
        if edge:
            for info_edge in edge:
                cv2.drawContours(
                    chr_k, [info_edge['contour']], -1, (70, 255, 20), 3)
                # if aba == processos[0] and not trav:

                if edge_only == True:
                    return (tuple(info_edge['contour'][0])[1], height, 0, width)
                else:
                    offset_screw = round(info_edge['dimension'][0], 3)
                    cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), thickness=3)
                    #print(point_a[1])
                    #edge_analyze = imgAnalyse[point_a[1]: height, 0:width]
                #     edge_analyze = imgAnalyse[348: height, 0:width]
                #     pass
                # if aba == processos[1] and not trav:
                #     offset_screw = round(info_edge['dimension'][0], 3)
                #     cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                #                 (255, 255, 255), thickness=3)
        else:
            return offset_screw, chr_k
    return offset_screw, chr_k


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

mainConfig = Fast.readJson('Json/config.json')
HSVJson = mainConfig['Filtros']['HSV']
cap = cv2.VideoCapture(0)
cap.set(3, 3264)
cap.set(4, 2448)
while True:
    _, img = cap.read()
    cv2.imshow("Img", cv2.resize(img, None, fx=0.3, fy=0.3))
    cv2.waitKey(1)
exit()
_, Image = cap.read()
Quadrants = Op.meshImg(Image)
# Image = Quadrants[line][column]

p1 = tuple(map(opr.add, map(opr.mul, (((Quadrants[line][column]).shape[:2])[
           ::-1]), (column, line)), (-500, -300)))
p2 = tuple(map(opr.add, map(opr.mul, ((
    (Quadrants[line-1][column-1]).shape[:2])[::-1]), (column+1, line+1)), (500, -400)))
Image = Image[p1[1]:p2[1], p1[0]:p2[0]]
cv2.imshow("Image", Image)
cv2.waitKey(0)
Processos = ['Edge', 'Screw']

borda = findScrew(Image, HSVJson, mainConfig, ['Edge'], edge_only=True)
print(borda)
while cv2.waitKey(1) != 27:
    _, Image = cap.read()
    Quadrants = Op.meshImg(Image)
    cv2.rectangle(Image, p1, p2, (0, 0, 255), 5)
    cv2.imshow('Image_Original', cv2.resize(
                Image, None, fx=0.35, fy=0.35))
    
    Image = Image[p1[1]:p2[1], p1[0]:p2[0]]
    h_min = cv2.getTrackbarPos("H Min", "Controle")
    s_min = cv2.getTrackbarPos("S Min", "Controle")
    v_min = cv2.getTrackbarPos("V Min", "Controle")

    h_max = cv2.getTrackbarPos("H Max", "Controle")
    s_max = cv2.getTrackbarPos("S Max", "Controle")
    v_max = cv2.getTrackbarPos("V Max", "Controle")

    Amin = cv2.getTrackbarPos("A Min", "Controle")
    Amax = cv2.getTrackbarPos("A Max", "Controle")
    _, img2 = findScrew(Image, HSVJson, mainConfig, ['Screw'], edge_only=borda, manual=False)

    cv2.imshow("img", cv2.resize(img2, None, fx=0.5, fy=0.5))
    
print(f'"h_min":{h_min}, "s_min":{s_min}, "v_min":{v_min},')
print(f'"h_max":{h_max}, "s_min":{s_max}, "v_max":{v_max},')