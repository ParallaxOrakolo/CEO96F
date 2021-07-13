class teste():
    def __init__(self, nome):
        self.nome = nome

    def echo(self):
        print(self.nome)
    
    def stop(self):
        print(f" {self.nome} parou")

    def join(self):
        print(f" {self.nome} join")

    def start(self):
        print(f" {self.nome} start")


for x in range(1,3):
    globals()["t"+str(x)] = teste(str(x))

print(globals())
for x in range(3):
    try:
        globals()["t"+str(x)].join()
    except KeyError as Ke:
        print(Ke)
        pass
