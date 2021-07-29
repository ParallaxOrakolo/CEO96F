
#S = raiz(l^2 - 4h^2)
#S = raiz((l**2) - (4*(h**2)))
#S = ((l^2) - (4*(h^2)))^0.5
#S = ((l^2))^0.5 - (4*(h^2))^0.5
#S-((l^2))^0.5 = -(4*(h^2))^0.5
# S^2 =L^2 - 4H^2
# RAIZ((S^2-L^2)/-4) = H


def NLinearRegression(x, c=160, aMin=152.61, reverse=False):
    if not reverse:
        return round(aMin-(c**2 - ((c**2-aMin**2)**0.5+x)**2)**0.5, 2)
    else:
        return round(((c**2 - (aMin-x )**2)**0.5)-(c**2- aMin**2)**0.5, 2)

    
    #return round((0.0051*(x**2)) + (0.302*x) + (0.5339), 2)        # 19/07 - 2/2 0->30
    #return round((-0.0231*(x**2))+(2.4001*x)+0.4472, 2)            # Reversa 19/07
    #return round(((x**2)*0.0035)+(0.3518*x)+0.1181,2)              # 20/07 - 0,2/0,2 0 -> 6,2
    

z = NLinearRegression(float(input()), reverse=True)
print(z)
print(NLinearRegression(z))
exit()      
import asyncio
from time import sleep

Sair = False
async def A():
    auto_exit = False
    contador = 0
    while not Sair and not auto_exit:
        contador +=1
        sleep(1)
        print("A:", contador)
        if contador >= 10:
            print("Auto Exit")
            auto_exit = True


async def B():
    for x in range(5,-1,-1):
        sleep(1)
        print(x)

async def Start():
     await A()

async def SUB():
    asyncio.run(Start())

async def RUN():
    await SUB()
    print("~~"*20)


asyncio.run(RUN())