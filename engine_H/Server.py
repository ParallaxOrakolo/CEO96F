from FastFunctions import Hex2HSVF, HSVF2Hex
import json


def printJson(jsons):
    print(json.dumps(jsons, sort_keys=True, indent=4))

HSVF2Hex(Hex2HSVF("#47a6ff", print=True), print=True)

camera={
    "process": "hole",
    "filters": {
        "hole": {
            "name": "hole",
            "area": [10, 20],
            "gradient": {
                "color": "#a02727",
                "color2": "#e261ae"
            },
            "hsv":{
                "hue": [2, 50],
                "sat": [0, 250],
                "val": [30, 50]
                }
            },
        "screw": {
            "name": "screw",
            "area": [10, 20],
            "gradient": {
                "color": "#a02727",
                "color2": "#e261ae"
            },
            "hsv":{
                "hue": [2, 50],
                "sat": [0, 250],
                "val": [30, 50]
                }
            },

        "normal": {
            "name": "normal",
            "area": [10, 20],
            "gradient": {
                "color": "#a02727",
                "color2": "#e261ae"
            },
            "hsv":{
                "hue": [2, 50],
                "sat": [0, 250],
                "val": [30, 50]
                }
            }
    },
}

Filtros = {
    "HSV": {
        "hole": {
            "Application": "hole",
            "Valores": {
                "lower": {
                    "h_min": 15,
                    "s_min": 0,
                    "v_min": 172
                },
                "upper": {
                    "h_max": 71,
                    "s_max": 152,
                    "v_max": 255
                }
            }
        },
        "screw": {
            "Application": "screw",
            "Valores": {
                "lower": {
                    "h_min": 0,
                    "s_min": 0,
                    "v_min": 43
                },
                "upper": {
                    "h_max": 164,
                    "s_max": 87,
                    "v_max": 243
                }
            }
        },
        "normal": {
            "Application": "normal",
            "Valores": {
                "lower": {
                    "h_min": 0,
                    "s_min": 0,
                    "v_min": 0
                },
                "upper": {
                    "h_max": 255,
                    "s_max": 255,
                    "v_max": 0
                }
            }
        }
    }
}

def setCameraFilter():
    for process in Filtros["HSV"]:
        process = Filtros["HSV"][process]
        tags = "lower", "upper"
        index = 0
        colorRange = []
        for tag in tags:
            colorItem = []
            for id, item in process["Valores"][tag].items():
                names = ["hue", "sat", "val"]
                for n in names:
                    if id[0:1] in n:
                        id = n
                        break
                camera["filters"][process["Application"]]["hsv"][id][index] = item
                colorItem.append(item)
            colorRange.append(colorItem)
            index = 1
        camera["filters"][process["Application"]]["gradient"]["color"] = HSVF2Hex(colorRange[0])
        camera["filters"][process["Application"]]["gradient"]["color2"] = HSVF2Hex(colorRange[1])

#["Valores"]["lower"]

def updateCamera(jsonPayload):
    newColors = []
    for filters in jsonPayload["filters"]:
        colorGroup= []
        filterName = filters
        filters = jsonPayload["filters"][filters]["gradient"]
        for hexColor in filters:
            hexColor = filters[hexColor]
            colorGroup.append(Hex2HSVF(hexColor, print=True))
        newColors.append(colorGroup)
        for index in range(len(colorGroup)):
            jsonPayload["filters"][filterName]["hsv"]["hue"][index] = colorGroup[index][0]
            jsonPayload["filters"][filterName]["hsv"]["sat"][index] = colorGroup[index][1]
            jsonPayload["filters"][filterName]["hsv"]["val"][index] = colorGroup[index][2]
    return jsonPayload
setCameraFilter()
camera = updateCamera(camera)
exit()
# NewMax = 255
# NewMin = 0

# OldRange = (OldMax - OldMin)  
# NewRange = (NewMax - NewMin)  
# NewValue = (((0.5 - OldMin) * NewRange) / OldRange) + NewMin
# print(color.hsv[1], "-> ", NewValue)
# print(color2.hsv)
# exit()

def ScanWebcam(*args):
    for X in range(*args):
        cap = cv2.VideoCapture(X)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(1280))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(720))
        if cap.isOpened():
            for Z in range(10):
                _, img = cap.read()
                print(X)
                cv2.imshow("Cam ID:"+str(X), img)
                cv2.waitKey(5)
            print("ID: [" + str(X) + "] disponível")
        else:
            print("ID: [" + str(X) + "] Inválido")


def OpenWebcam(ID, **kargs):
    cap = cv2.VideoCapture(ID, cv2.CAP_DSHOW)
    Pfx = kargs.get('Prefix')
    Sfx = kargs.get('Sufix')
    path = kargs.get('Save')
    imgName = kargs.get('ImgName')
    idn = ' [ID: ' + str(ID) + '] '
    tecla = kargs.get('Trigger')
    if Sfx or Pfx:
        if Pfx and Sfx:
            name = (str(Pfx) + idn + str(Sfx))
        elif not Sfx:
            name = (str(Pfx) + idn)
        else:
            name = (idn + str(Sfx))
    else:
        name = idn
    if path:
        print("Aperte "+ tecla +" para salvar em "+str(path))
    if cap.isOpened():
        while True:
            _, img = cap.read()

            cv2.imshow(name, img)
            key = cv2.waitKey(1)
            try:
                print(ord(key))
            except TypeError:
                pass
            if key == 27:
                cv2.destroyAllWindows()
                break
            elif key == ord(tecla):
                cv2.imwrite('../Master/Imagens/Teste/'+str(imgName)+'.jpg', img)




ScanWebcam(10)

