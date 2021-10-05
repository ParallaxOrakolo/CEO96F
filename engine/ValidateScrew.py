import cv2
import OpencvPlus as Op
import FastFunctions as Fast
import numpy as np

#Op.ControlWindow((0, 179), (0, 69), (58, 144), (8000, 60000))
#Op.ControlWindow((0, 34), (116, 210), (0, 140), (3600, 6500))
Op.ControlWindow((0, 286), (0, 86), (39, 218), (8000, 6200))
def Process_Imagew_Scew(frame, lower, upper, AreaMin, AreaMax, name="ScrewCuts"):

    frames = frame.copy()
    #cv2.drawMarker(frames, (int(frames.shape[1]/2), int(frames.shape[0]/2)), (0,0,255), thickness=30, markerSize=100000)
    img_draw = frames.copy()
    # cv2.imshow("img_draw_original", cv2.resize(img_draw, None, fx=0.35, fy=0.35))
    finds = 0
    for Pontos in globals()[name]:
        pa, pb = tuple(Pontos["P0"]), (Pontos["P0"][0]+Pontos["P1"][0],
                                       Pontos["P0"][1]+Pontos["P1"][1])

        cv2.drawMarker(img_draw, pa, (255, 50, 0), thickness=10)
        cv2.drawMarker(img_draw, pb, (50, 255, 0), thickness=10)
        cv2.rectangle(img_draw, pa, pb, (255, 50, 255), 10)
        show = frames[Pontos["P0"][1]:Pontos["P0"][1] + Pontos["P1"][1],
                   Pontos["P0"][0]:Pontos["P0"][0] + Pontos["P1"][0]]
        
        mask = Op.refineMask(Op.HSVMask(show, lower, upper), kerenelA=(10,10))
        Cnt_A, _ = Op.findContoursPlus(mask, AreaMin_A=AreaMin, AreaMax_A=AreaMax)
        
        show = cv2.bitwise_or(show, show, None, mask)
        if Cnt_A:
            finds += len(Cnt_A)
            for info in Cnt_A:
                cv2.drawContours(show, [info['contour']], -1, (0, 255, 0), thickness=10,
                                 lineType=cv2.LINE_AA)

                for pp in range(len(info['contour'])):
                    info['contour'][pp][0] += pa[0]
                    info['contour'][pp][1] += pa[1]

                cv2.drawContours(img_draw, [info['contour']], -1, (0, 255, 0), thickness=10,
                                 lineType=cv2.LINE_AA)

        img_draw[Pontos["P0"][1]:Pontos["P0"][1] + show.shape[0],
                Pontos["P0"][0]:Pontos["P0"][0] + show.shape[1]] = show
    cv2.putText(img_draw, str(finds), (200, 100), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 0), 10)
    return img_draw, finds

def Process_Image_Hole(frame, areaMin, areaMax, perimeter, HSValues):
    img_draw = frame.copy()
    for Pontos in HoleCuts:
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #            Corta a imagem e faz as marcações               #

        show = frame[Pontos["P0"][1]:Pontos["P0"][1] + Pontos["P1"][1],
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
    #cv2.imshow("show", cv2.resize(show, None, fx=0.25, fy=0.25))
    # cv2.imshow("draw", cv2.resize(img_draw, None, fx=0.25, fy=0.25))
    # cv2.waitKey(1)
    return Resultados, R, per, img_draw

def findHole(imgAnalyse, minArea, maxArea, c_perimeter, HSValues, fixed_Point, escala_real=4.4):
    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    for filter_values in HSValues:
        locals()[filter_values] = np.array(
            Op.extractHSValue(HSValues, filter_values))
    mask = Op.refineMask(Op.HSVMask(imgAnalyse, locals()
                         ['lower'], locals()['upper']))
    mask_inv = cv2.bitwise_not(mask)
    chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
    distances = []
    #edge = findCircle(mask, minArea, maxArea, c_perimeter)
    edge, null = Op.findContoursPlus(
            mask_inv, AreaMin_A=minArea, AreaMax_A=maxArea)
    #cv2.imshow("Mascara", cv2.resize(mask, None, fx=0.3, fy=0.3))
    if edge:
        for info_edge in edge:
            try:
                if 20 <= int(info_edge['dimension'][0]/2) <= 80:

                    cv2.drawMarker(chr_k,(info_edge['centers'][0]), (0,255,0), thickness=3)
                    cv2.circle(chr_k, (info_edge['centers'][0]), int(info_edge['dimension'][0]/2),
                    (36, 255, 12), 2)
                    
                    cv2.line(chr_k, (info_edge['centers'][0]), fixed_Point, (255, 0, 255), thickness=3)

                    cv2.line(chr_k, (info_edge['centers'][0]),
                            (int(info_edge['centers'][0][0]), fixed_Point[1]), (255, 0, 0), thickness=3)

                    cv2.line(chr_k, (int(info_edge['centers'][0][0]), fixed_Point[1]), fixed_Point, (0, 0, 255), thickness=2)
                    distance_to_fix = (round(((info_edge['centers'][0][0] - fixed_Point[0])*(escala_real/(info_edge['dimension'][0]))), 2),
                                    round(((info_edge['centers'][0][1] - fixed_Point[1])*(escala_real/(info_edge['dimension'][0]))), 2))

                    # cv2.putText(chr_k, str(distance_to_fix[1]), (int(Circle['center'][0]), int(Circle['center'][1] / 2)),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    # cv2.putText(chr_k, str(distance_to_fix[0]), (int(Circle['center'][0] / 2), int(fixed_Point[1])),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    # cv2.putText(chr_k, str(Circle["id"]), (int(Circle["center"][0]), int(Circle["center"][1])),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

                    distances.append(distance_to_fix)
                    distances = list(dict.fromkeys(distances))
                    distances.sort(key = sortSecond)
                    cv2.putText(chr_k, str(len(distances)-1), (info_edge['centers'][0]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 50, 100), 5)
                    cv2.drawContours(chr_k, [info_edge['contour']], -1, (255, 255, 255), 3)
            except KeyError:
                print("KeyError:", info_edge)
    try:
        return distances, chr_k, (info_edge['dimension'][0])
    except UnboundLocalError:
        return distances, chr_k, (0)


def sortSecond(val):
    return val[1] 


# cap = cv2.VideoCapture(1)
# cap.set(3, 3264)
# cap.set(4, 2448)
# # _, show = cap.read()
# ScrewCuts = Fast.readJson("../engine/Json/ScrewCuts.json")
ScrewCuts = Fast.readJson("../engine/Cuts.json")
# HoleCuts = Fast.readJson("../engine/Json/HoleCuts.json")
quem = ["0mcG6", "1snHl","CBjzQ"]
id = 2
quant = 3

#img = cv2.imread(f"../engine/Images/Process/{quem[id]}/validar/{quant}_normal.jpg")
# img = cv2.imread('c:/Users/55419/Trabalho/Parallax/GitRepos/CEO96F/engine/Images/Errado_1_1_normal.jpg')
# img = cv2.imread('c:/Users/55419/Trabalho/Parallax/GitRepos/CEO96F/engine/Images/0_3_normal.jpg')
img = cv2.imread(f"../engine/Images/Process/m5GeS_258/validar/12/normal/4.jpg")
imgs = Op.Rois(img, 6, 0.25)
while cv2.waitKey(1) != 27:
    #_, img = cap.read()
    
    Values, Values2 = Op.GetControlWindow()
    frame, __ = Process_Imagew_Scew(img, Values['lower'], Values['upper'], Values["a_min"], Values["a_max"])
    # _, _, _, frame = Process_Image_Hole(img,Values["a_min"], Values["a_max"], 4, Values2)
    cv2.imshow("show", cv2.resize(frame, None, fx=0.3, fy=0.3))
print(Values["a_min"], Values["a_max"], Values2)
exit()
while cv2.waitKey(1) != 27:
    #img = cv2.imread("../engine/Images/1.jpg")
    _, img = cap.read()
    img_draw = img.copy()
    imgs = []
    finds = 0
    for Pontos in ScrewCuts:

        show = img[Pontos["P0"][1]:Pontos["P0"][1] + Pontos["P1"][1],
                   Pontos["P0"][0]:Pontos["P0"][0] + Pontos["P1"][0]]

        pa, pb = tuple(Pontos["P0"]), (Pontos["P0"][0]+Pontos["P1"][0],
                                       Pontos["P0"][1]+Pontos["P1"][1])

        cv2.drawMarker(img_draw, pa, (255, 50, 0), thickness=10)
        cv2.drawMarker(img_draw, pb, (50, 255, 0), thickness=10)
        cv2.rectangle(img_draw, pa, pb, (255, 50, 255), 10)

        Values = Op.GetControlWindow()
        mask = Op.refineMask(Op.HSVMask(show, Values["lower"], Values["upper"]), kerenelA=(10,10))
        Cnt_A, _ = Op.findContoursPlus(mask, AreaMin_A=Values["a_min"], AreaMax_A=Values["a_max"])

        show = cv2.bitwise_or(show, show, None, mask)
        if Cnt_A:
            finds += 1
            for info in Cnt_A:
                cv2.drawContours(show, [info['contour']], -1, (0, 255, 0), thickness=10,
                                 lineType=cv2.LINE_AA)

                for pp in range(len(info['contour'])):
                    info['contour'][pp][0] += pa[0]
                    info['contour'][pp][1] += pa[1]

                cv2.drawContours(img_draw, [info['contour']], -1, (0, 255, 0), thickness=10,
                                 lineType=cv2.LINE_AA)

        cv2.imshow(f"Img_{Pontos}", show)
        img_draw[Pontos["P0"][1]:Pontos["P0"][1] + show.shape[0],
                Pontos["P0"][0]:Pontos["P0"][0] + show.shape[1]] = show
    cv2.putText(img_draw, str(finds), (200, 100), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 0), 10)
    cv2.imshow(f"Draw_Copy", cv2.resize(img_draw, None, fx=0.25, fy=0.25))
