import FastFunctions as Fast
import timeit
import threading
from time import sleep
t_atual = 0
tantigo = 0
while True:
    t0 = timeit.default_timer()
    sleep(0.5)
    tantigo, t_atual  = t_atual - tantigo, timeit.default_timer() - t0
    print(round(tantigo,4), round(t_atual,4))