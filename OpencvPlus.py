import cv2
import numpy as np
import math


# Organiza todos os valores de uma matriz bidimensional em ordem crescente.
def order_points_old(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


# Concatena uma lista de mascaras.
def loopBitwiseOr(vetor):
    resposta = []
    for n in range(int(len(vetor) / 2)):
        valor = cv2.bitwise_or(vetor[n + n], vetor[n * 2 + 1])
        resposta.append(valor)
    if len(vetor) % 2 == 1:
        resposta.append(vetor[len(vetor) - 1])
    return resposta


# Extrai os valores de um grupo de vetores.
def extractHSValue(HSVector, key):  # Função que extrai e orgazina alguns valores dentro de um vetor
    data = HSVector[key]
    return np.array([int(data[0]), int(data[1]), int(data[2])])


# Procura por contornos com área pré determinada, e retorna um dicionário com vários informações uteis.
def findContoursPlus(image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE, AreaMin_A=100, AreaMax_A=00,
                     AreaMin_B=100, AreaMax_B=00):
    cnts2, hierarchy = cv2.findContours(image, mode=mode, method=method)
    outPut_A = outPut_B = []
    try:
        hierarchy = hierarchy[0]
        for component in zip(cnts2, hierarchy):
            currentContour = component[0]
            area = cv2.contourArea(currentContour)
            currentHierarchy = component[1]
            if AreaMin_A < area < AreaMax_A:
                xA, yA, wA, hA = cv2.boundingRect(currentContour)
                boxA = np.int0(cv2.boxPoints(cv2.minAreaRect(currentContour)))
                boxOrded = order_points_old(np.array(boxA, dtype="float32"))
                bxA = boxOrded[2][0] - boxOrded[1][0]
                axA = boxOrded[1][1] - boxOrded[2][1]
                byA = boxOrded[0][0] - boxOrded[1][0]
                ayA = boxOrded[1][1] - boxOrded[0][1]
                alturaA = math.sqrt(pow(axA, 2) + pow(bxA, 2))
                larguraA = math.sqrt(pow(ayA, 2) + pow(byA, 2))
                momentsA = cv2.moments(currentContour)
                cxA = int(momentsA["m10"] / momentsA["m00"])
                cyA = int(momentsA["m01"] / momentsA["m00"])
                centro_momentsA = (cxA, cyA)
                centro_boxA = (larguraA / 2 + xA, alturaA / 2 + yA)
                if currentHierarchy[3] < 0:
                    lesst3A = True
                else:
                    lesst3A = False
                outPut_A.append(
                    {"class": 'A', "boundRect": [(xA, yA), (wA, hA)], "dimension": [alturaA, larguraA], "contour": boxA,
                     'hierarchy': [lesst3A, currentHierarchy], "centers": [centro_momentsA, centro_boxA]})
            elif AreaMin_B < area < AreaMax_B:
                xB, yB, wB, hB = cv2.boundingRect(currentContour)
                boxB = np.int0(cv2.boxPoints(cv2.minAreaRect(currentContour)))
                boxOrded = order_points_old(np.array(boxB, dtype="float32"))
                bxB = boxOrded[2][0] - boxOrded[1][0]
                axB = boxOrded[1][1] - boxOrded[2][1]
                byB = boxOrded[0][0] - boxOrded[1][0]
                ayB = boxOrded[1][1] - boxOrded[0][1]
                alturaB = math.sqrt(pow(axB, 2) + pow(bxB, 2))
                larguraB = math.sqrt(pow(ayB, 2) + pow(byB, 2))
                momentsB = cv2.moments(currentContour)
                cx = int(momentsB["m10"] / momentsB["m00"])
                cy = int(momentsB["m01"] / momentsB["m00"])
                centro_momentsB = (cx, cy)
                centro_boxB = (larguraB / 2 + xB, alturaB / 2 + yB)
                if currentHierarchy[3] < 0:
                    lesst3B = True
                else:
                    lesst3B = False
                outPut_B.append(
                    {"class": 'B', "boundRect": [xB, yB, wB, hB], "dimension": [alturaB, larguraB], "contour": boxB,
                     'hierarchy': [lesst3B, currentHierarchy], "centers": [centro_momentsB, centro_boxB]})
        return outPut_A, outPut_B
    except TypeError:
        return [], []


# Cria uma mascara HSV apartir de um range pré-determinado.
def HSVMask(img, lower, upper, invert=False):
    return cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower, upper)


# Reduz ruídos os ruidos da mascara.
def refineMask(maskToRefine, kerenelA=(3, 3), kernelB=(2, 2)):
    return cv2.morphologyEx(cv2.morphologyEx(maskToRefine, cv2.MORPH_CLOSE, (np.ones(kerenelA, np.uint8))),
                            cv2.MORPH_OPEN,
                            (np.ones(kernelB, np.uint8)))


# Recorta uma imagem em uma matriz de 'n' retangulos iguais.
def meshImg(img, nRows=3, mCols=3):
    rois = []
    for i in range(0, nRows):
        lines = []
        for j in range(0, mCols):
            roi = img[
                  int(i*img.shape[0]/nRows):int(i*img.shape[0]/nRows + img.shape[0]/nRows),
                  int(j*img.shape[1]/mCols):int(j*img.shape[1]/mCols + img.shape[1]/mCols)
                  ]
            lines.append(roi)
        rois.append(lines)
    return rois


# Concatena Horizontal ou verticalmente mais de uma imagem.
def concatImg(imgMeshed, index, p1, p2, **orientation):
    pc = [x for x in range(p1, p2 + 1)]
    img = np.zeros(2)
    if orientation.get('h') or orientation.get('H'):
        for x in pc:
            if x == pc[0]:
                img = np.concatenate((imgMeshed[index][x], imgMeshed[index][x + 1]), axis=1)
            elif x != pc[len(pc)-1]:
                img = np.concatenate((img, imgMeshed[index][x + 1]), axis=1)
    else:
        for x in pc:
            if x == pc[0]:
                img = np.concatenate((imgMeshed[x][index], imgMeshed[x + 1][index]), axis=0)
            elif x != pc[len(pc) - 1]:
                img = np.concatenate((img, imgMeshed[x + 1][index]), axis=0)
    return img


# Tira uma foto
def takeSnapshot(cameraID):  # Função que lê e retorna a imagem presente na camera
    if type(cameraID) != cv2.VideoCapture:
        image_status, image = (cv2.VideoCapture(cameraID, cv2.CAP_DSHOW)).read()
    else:
        image_status, image = cameraID.read()
    if image_status:
        return image
    else:
        # Todo: Raise an Exception
        exit('Camera não encontrada, verifique a conexão.')
