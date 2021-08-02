import cv2
import OpencvPlus as Op
import FastFunctions as Fast

Op.ControlWindow((0, 179), (0, 69), (58, 144), (8000, 60000))
def Process_Imagew_Scew(frame, lower, upper, AreaMin, AreaMax, name="ScrewCuts"):

    frames = frame.copy()
    cv2.drawMarker(frames, (int(frames.shape[1]/2), int(frames.shape[0]/2)), (0,0,255), thickness=30, markerSize=100000)
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

cap = cv2.VideoCapture(1)
cap.set(3, 3264)
cap.set(4, 2448)
_, show = cap.read()
ScrewCuts = Fast.readJson("../engine_H/Json/ScrewCuts.json")
ScrewCuts = Fast.readJson("../engine_H/Cuts.json")
quem = ["0mcG6", "1snHl","CBjzQ"]
id = 2
quant = 3

img = cv2.imread(f"../engine_H/Images/Process/{quem[id]}/validar/{quant}_normal.jpg")
#imgs = Op.Rois(img, 4, 0.25)
while cv2.waitKey(1) != 27:
    #_, img = cap.read()
    
    Values = Op.GetControlWindow()
    _, __ = Process_Imagew_Scew(img, Values['lower'], Values['upper'], Values["a_min"], Values["a_max"])
    cv2.imshow("show", cv2.resize(_, None, fx=0.3, fy=0.3))
exit()
while cv2.waitKey(1) != 27:
    #img = cv2.imread("../engine_H/Images/1.jpg")
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
