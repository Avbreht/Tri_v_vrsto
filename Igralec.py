
class Igralec():
    def __init__(self,gui,ime,barva):
        self.gui = gui
        self.ime = ime
        self.barva = barva

    def klik(self, i,j):
        """Igralec mora izvesti potezo"""
        self.gui.izvediPotezo(i,j)

    def igraj(self):
        pass

    def prekini(self):
        pass
