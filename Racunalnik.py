import random
import Igra
import Main
import threading

class Racunalnik():
    def __init__(self,gui,ime,barva,tezavnost):
        self.gui = gui
        self.barva = barva
        self.ime = ime
        self.tezavnost = tezavnost

        self.algoritem = Mini_Max(tezavnost)

        print("initet racunalnik",gui,ime,barva,tezavnost)

    def klik(self, i,j):
        pass

    def igraj(self):
        self.mislec = threading.Thread(target= lambda: self.algoritem.izracuna_potezo(self.gui.igra.kopija()))
        # print(self.mislec)
        self.mislec.start()
        self.gui.igralna_plosca.after(500, self.preveri_potezo)

    def preveri_potezo(self):
        print("preverjam potezo")
        if self.mislec is None or self.gui.igra.stanje[1] is None:
            return
        if self.algoritem.poteza is not None:
            px,py = self.algoritem.poteza
            print("igram,potezo",px,py)
            #self.gui.igra.igrajPotezo(px,py)
            self.gui.izvediPotezo(px,py)
            self.mislec = None
        else:
            self.gui.igralna_plosca.after(100, self.preveri_potezo)

    def prekini(self):
        pass


class Mini_Max():
    def __init__(self,zahtevnost):
        self.zahtevnost = zahtevnost
        self.igra = None
        self.jaz = None
        self.poteza = None

        self.Zmaga = 100000000
        self.Neskonco = self.Zmaga +1

    def izracuna_potezo(self,igra):
        self.igra = igra
        self.jaz = self.igra.naPotezi
        self.poteza = None
        if self.zahtevnost == 1:
            poteza = self.random_placer()
        elif self.zahtevnost == 2:
            poteza,vrednost = self.minimax(True)
        else:
            raise("random error")
        self.igra = None
        self.jaz = None
        self.poteza = poteza


    def minimax(self,maksimiziramo):
        """
        Izracuna "optimalno" potezo, ki jo mora racunalnik odigrati,
        ob predpostavki da njegov nasprotnik igra optimalno
        """
        stanje = self.igra.stanje
        if stanje == self.igra.ZMAGA:
            if self.igra.zmagovalec == self.jaz:
                return None,self.Zmaga
            else:
                return None,-self.Zmaga
        elif stanje == self.igra.NIHCENEZMAGA:
            return None,0
        else:
            if maksimiziramo:
                moznepoteze = self.igra.moznePoteze()
                random.shuffle(moznepoteze)
                top_poteza = None
                top_vred = -self.Neskonco
                for px,py in moznepoteze:
                    self.igra.igrajPotezo(px,py)
                    vrednost = self.minimax(not maksimiziramo)[1]
                    self.igra.razveljavi()
                    if vrednost > top_vred:
                        top_vred = vrednost
                        top_poteza = (px,py)
            else:
                moznepoteze = self.igra.moznePoteze()
                random.shuffle(moznepoteze)
                top_poteza = None
                top_vred = self.Neskonco
                for px,py in moznepoteze:
                    self.igra.igrajPotezo(px,py)
                    vrednost = self.minimax(not maksimiziramo)[1]
                    self.igra.razveljavi()
                    if vrednost < top_vred:
                        top_vred = vrednost
                        top_poteza = (px,py)
        return top_poteza,top_vred





    def random_placer(self):
        moznepoteze = self.igra.moznePoteze()
        a = len(moznepoteze)
        b = random.randint(0,a-1)
        #print("nakljucn leement",b)
        return moznepoteze[b]



#     # Testr
#     def test(self):
#         self.igra =Igra.Igra()
#         self.jaz = self.igra.naPotezi
#
#
#         print(self.minimax(True))
#
#
# a = Mini_Max(10)
# a.test()
#
#


