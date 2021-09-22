def mm2coordinate(x, c=160, aMin=148.509, reverse=False):
    if not reverse:
        r = aMin-(c**2 - ((c**2-aMin**2)**0.5+x)**2)**0.5
 #       edit(f"Convertendo {x} em {r} | reverse=False\n")
        return r
    else:
        r = ((c**2 - (aMin-x)**2)**0.5)-(c**2 - aMin**2)**0.5
#        edit(f"Convertendo {x} em {r} | reverse=True\n")
        return r

print(mm2coordinate(mm2coordinate(3.61, reverse=True)+2.45))
print(mm2coordinate(mm2coordinate(3.38, reverse=True)-4.103))


# 4.58 --- 0.0
# 3.38     4.103