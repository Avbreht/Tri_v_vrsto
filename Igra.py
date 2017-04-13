import copy
import queue

class Igra():

    def __init__(self):
        self.IGRALEC_O = "O"
        self.IGRALEC_X = "X"
        self.NIHCENEZMAGA = "Nihče ni zmagovalec"
        self.NIKONEC = "Ni konec"
        self.ZMAGA = "Zmaga"

        self.plosca = [[None,None,None],[None,None,None],[None,None,None]]
        self.naPotezi = self.IGRALEC_O

        self.stanje = self.NIKONEC
       # self.logIgre = list()

        self.zgodovina = queue.LifoQueue()

        self.zmagovalec = None


    zmagovalneTrojke = [
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)]
    ]

    def kopija(self):
        kopija = Igra()
        kopija.plosca = copy.deepcopy(self.plosca)
        kopija.naPotezi = self.naPotezi
        return kopija

    def razveljavi(self):
        a,px,py = self.zgodovina.get()
        self.naPotezi = a
        self.plosca[px][py] = None

    def moznePoteze(self):
        veljavne = list()
        for i in range(3):
            for j in range(3):
                if self.plosca[i][j] == None:
                    veljavne.append((i,j))
        return veljavne

    def igrajPotezo(self, i,j):
        if i > 2 or j > 2 or (self.plosca[i][j] != None):
            return None
        # assert self.plosca[i][j] == None, "Neveljavna poteza"
        self.plosca[i][j] = self.naPotezi
        self.zgodovina.put((self.naPotezi,i,j))
        zmagovalec, kako = self.stanjeIgre()
        if zmagovalec == self.NIKONEC:
            self.naPotezi = self.Nasprotnik(self.naPotezi)
            self.stanje = self.NIKONEC
        else:
            self.naPotezi = None
            if zmagovalec == self.NIHCENEZMAGA:
                self.stanje = self.NIHCENEZMAGA
            else:
                self.stanje = self.ZMAGA
                self.zmagovalec = zmagovalec
        return (zmagovalec, kako)


    def stanjeIgre(self):
        for ((x1,y1),(x2,y2),(x3,y3)) in Igra.zmagovalneTrojke:
            polje1 = self.plosca[x1][y1]
            if self.plosca[x2][y2] == self.plosca[x3][y3] == polje1 and polje1 != None:
                return polje1, ((x1,y1),(x2,y2),(x3,y3))
        for vrstica in self.plosca:
            for element in vrstica:
                if element == None:
                    return self.NIKONEC, None
        return self.NIHCENEZMAGA, None

    def Nasprotnik(self,igralec):
        if igralec == self.IGRALEC_X:
            return self.IGRALEC_O
        elif igralec == self.IGRALEC_O:
            return self.IGRALEC_X
        assert False, "Neveljaven nasprotnik"