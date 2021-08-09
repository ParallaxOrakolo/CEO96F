from FastFunctions import Hex2HSVF, HSVF2Hex, readJson, writeJson
from random import randint, random
import datetime
import asyncio
import json

def printJson(jsons):
    print(json.dumps(jsons, sort_keys=True, indent=4))
production = readJson("Json/production.json")
current_time  = datetime.datetime.now()
for n in range(randint(5, 10)):
    production["production"]["today"]["timesPerCicles"].append(random())

if int(production["production"]["today"]["day"]) != int(current_time.day):
    production["production"]["yesterday"] = production["production"]["today"]
    # Zera o dia de hoje
    production["production"]["today"] = {"day": int(current_time.day),"total": 0,"rigth": 0,"wrong": 0,"timePerCicle": 0,"timesPerCicles": []}
    production["production"]["dailyAvarege"]["week_times"].append(production["production"]["yesterday"]["timePerCicle"])
    production["production"]["dailyAvarege"]["week_total"].append(production["production"]["yesterday"]["total"])
    production["production"]["dailyAvarege"]["week_rigth"].append(production["production"]["yesterday"]["rigth"])
    production["production"]["dailyAvarege"]["week_wrong"].append(production["production"]["yesterday"]["wrong"])
    week_time = production["production"]["dailyAvarege"]["week_times"]
    week_total = production["production"]["dailyAvarege"]["week_total"]
    week_rigth = production["production"]["dailyAvarege"]["week_rigth"]
    week_wrong = production["production"]["dailyAvarege"]["week_wrong"]
    appends = {"times":week_time, "total":week_total, "rigth":week_rigth, "wrong":week_wrong}
    if week_time:
        for k, v in appends.items():
            while len(v) > 5:
                v.pop(0)
            media =  sum(v) /len(v)
            print(k, v, media)
            production["production"]["dailyAvarege"][k] = media

valores = production["production"]["today"]["timesPerCicles"]
if valores:
    media =  sum(valores) /len(valores)
    production["production"]["today"]["timePerCicle"] = media
writeJson("Json/production.json", production)

exit()



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
    print("Usando valores definidos no arquivo para setar o payload inicial da camera.")
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


def setCameraHsv(jsonPayload):
    print("Alterando Payload da camera usando a  configuração do Front.")
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


def setFilterWithCamera(jsonOrigin, jsonPayload):
    print("Alterando valores da arquivo de configuração com base no payload da Camera")
    for _ in jsonPayload["filters"]:
        print("~"*20)
        #print(jsonOrigin["HSV"][_]["Valores"])
        lower = {}
        upper = {}
        for __ in jsonPayload["filters"][_]["hsv"]:
            lower[f"{__[0:1]}_min"] = jsonPayload["filters"][_]["hsv"][__][0]
            upper[f"{__[0:1]}_max"] = jsonPayload["filters"][_]["hsv"][__][1]
        Valoroes = {"lower":lower, "upper":upper}
        for k, v  in Valoroes.items():
            for k1, v1  in v.items():
                jsonOrigin["HSV"][_]["Valores"][k][k1] = v1

        print(f"{_}:", jsonOrigin["HSV"][_]["Valores"])

def updateCamera(payload):
    camera = setCameraHsv(payload)
    setFilterWithCamera(Filtros, camera)

setCameraFilter()
updateCamera(camera)
        

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




