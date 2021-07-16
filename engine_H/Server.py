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