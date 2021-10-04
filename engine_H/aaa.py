tt = 0
tr = 0
tw = 0
ttmin=0
ttmax=0

tdt = 0
tdr = 0
tdw = 0


ydt = 0
ydr = 0
ydw = 0


dat = 0
dar = 0
daw = 0
datpc = 0

dtw_ttpc = []
tdtcs = []
ydtcs = []
dtw_t = []
dtw_w = []
dtw_r = []
tdd=[]
ydd=[]
import FastFunctions as Fast
import numpy as np
production = Fast.readJson("Json/production.json")
modelo_atual ="1"
prodd = production["production"]["productionPartList"][int(modelo_atual)]["production"]
all_prodd = production["production"]["allParts"]["production"]
print("A")
for mod in production["production"]["productionPartList"]:
    tt += mod["production"]["total"]["total"]
    tr += mod["production"]["total"]["rigth"]
    tw += mod["production"]["total"]["wrong"]
    print("B")
    ttmin += mod["production"]["total"]["timePerCicleMin"]
    ttmax += mod["production"]["total"]["timePerCicleMax"]
    print("C")
    tdd.append(mod["production"]["today"]["day"])
    tdt += mod["production"]["today"]["total"]
    tdr += mod["production"]["today"]["rigth"]
    tdw += mod["production"]["today"]["wrong"]
    print("D")
    tdtcs += mod["production"]["today"]["timesPerCicles"]
    print("E")
    ydd.append(mod["production"]["today"]["day"])
    ydt += mod["production"]["yesterday"]["total"]
    ydr += mod["production"]["yesterday"]["rigth"]
    ydw += mod["production"]["yesterday"]["wrong"]
    ydtcs += mod["production"]["yesterday"]["timesPerCicles"]
    print("F")
    print("G")
    dat += mod["production"]["dailyAvarege"]["total"]
    dar += mod["production"]["dailyAvarege"]["rigth"]
    daw += mod["production"]["dailyAvarege"]["wrong"]
    datpc += mod["production"]["dailyAvarege"]["times"]
    print("H")
    dtw_t.append(np.array(mod["production"]["dailyAvarege"]["week_total"].copy(), dtype=object))
    dtw_r.append(np.array(mod["production"]["dailyAvarege"]["week_rigth"].copy(), dtype=object))
    dtw_w.append(np.array(mod["production"]["dailyAvarege"]["week_wrong"].copy(), dtype=object))
    dtw_ttpc.append(np.array(mod["production"]["dailyAvarege"]["week_times"].copy(), dtype=object))
    print("I")
print("J")
all_prodd["dailyAvarege"]["total"] = round(dat,2)
all_prodd["dailyAvarege"]["rigth"] = round(dat - daw,2)
all_prodd["dailyAvarege"]["wrong"] = round(daw,2)
all_prodd["dailyAvarege"]["times"] = round(datpc,2)
print("K")

print((np.around(np.average(np.array(dtw_t), axis=0).tolist())))
all_prodd["dailyAvarege"]["week_total"] = (np.around(np.average(np.array(dtw_t), axis=0).tolist())).tolist()
all_prodd["dailyAvarege"]["week_rigth"] = (np.around(np.average(np.array(dtw_r), axis=0).tolist())).tolist() 
all_prodd["dailyAvarege"]["week_wrong"] = (np.around(np.average(np.array(dtw_w), axis=0).tolist())).tolist()
all_prodd["dailyAvarege"]["week_times"] = (np.around(np.average(np.array(dtw_ttpc), axis=0).tolist())).tolist()
print("L")


all_prodd["total"]["total"] = tt
all_prodd["total"]["rigth"] = tt-tw
all_prodd["total"]["wrong"] = tw
print("M")

all_prodd["today"]["total"] = tdt
all_prodd["today"]["rigth"] = tdt-tdw
all_prodd["today"]["wrong"] = tdw
print( tdtcs)
all_prodd["today"]["timePerCicle"] = (np.around(np.average(np.array(tdtcs), axis=0).tolist())).tolist()
all_prodd["today"]["timesPerCicles"] = np.around(np.array(tdtcs)).tolist()
print("N")
all_prodd["yesterday"]["total"] = ydt
all_prodd["yesterday"]["rigth"] = ydt-ydw
all_prodd["yesterday"]["wrong"] = ydw
print("TT",ydtcs)
all_prodd["yesterday"]["timePerCicle"] = (np.around(np.average(np.array(ydtcs), axis=0).tolist())).tolist()
all_prodd["yesterday"]["timePerCicle"] = np.around(np.array(ydtcs)).tolist()
print("O")

all_prodd["total"]["timePerCicleMin"] = round(ttmin/len(production["production"]["productionPartList"]), 2)
all_prodd["total"]["timePerCicleMax"] = round(ttmax/len(production["production"]["productionPartList"]), 2)
print(all_prodd)
print("P")


    # if tdd.count(tdd[0]) == len(tdd):
    # if ydd.count(ydd[0]) == len(ydd):
        
    