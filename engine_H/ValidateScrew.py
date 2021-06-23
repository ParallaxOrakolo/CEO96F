import cv2
import OpencvPlus as Op
import FastFunctions as Fast
# # id = 6
# # Pos = 'A'
# # Picture = 0
# # path_to_file = f"Auto-Gen/{id}_Rand/"
# # with open(path_to_file+f'{Pos}/{id}_Rand_{Pos}.txt') as f:
# #     contents = f.readlines()

# Op.ControlWindow((37, 106), (183, 255), (20, 227), (6090, 65555))

# # nome = contents[Picture].rstrip()
# # p = f"Auto-Gen/{id}_Rand/{Pos}/{nome}.png"
# # SSW = 700
# # SSH = 700

# # SOW = 0
# # SOH = 200

# # LimitW = 300
# # LimitH = 300
# cap = cv2.VideoCapture(0)
# cap.set(3, 3264)
# cap.set(4, 2448)

ScrewCuts = Fast.readJson("../engine_H/Json/ScrewPoints.json")
# imgs = Op.Rois(show, 4, 0.25)


while cv2.waitKey(1) != 27:
    img = cv2.imread("../engine_H/Images/1.jpg")
    img_draw = img.copy()
    imgs = []
    finds = 0
    for Pontos in Cortes:

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
