import tkinter
import Igralec
import Igra
import Racunalnik

class Gui():

    def __init__(self,master):
        self.igralecO = None
        self.igralecX = None
        self.imeIgralecO = None
        self.imeIgralecX = None

        self.barvaIgralecX = 'forest green'
        self.barvaIgralecO = 'chocolate1'

        self.player1 = ""
        self.player2 = ""

        self.igra = None

        self.bg = 'LightYellow2' #'LemonChiffon'
        self.debelina = 3

        self.master = master

        self.width = 400
        self.height = 400

        master.protocol("WM_DELETE_WINDOW", lambda: self.zaprriOkno(master))

        # Menu addons
        menu = tkinter.Menu(master)
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_navodila = tkinter.Menu(menu)
        menu.add_cascade(label="Navodila", menu=menu_navodila)


        menu_navodila.add_command(label="Navodila", command=self.okno_navodila)
        menu_igra.add_command(label="Nova igra", command=self.izbira_nove_igre)
        master.config(menu=menu)

        # Siri part
        self.Siri = tkinter.StringVar(master, master)
        tkinter.Label(master, textvariable=self.Siri,font=("Helvetica", 14)).grid(row=0, column=0)

        self.igralna_plosca = tkinter.Canvas(self.master, width=self.width, height=self.height, bg=self.bg,relief=tkinter.SUNKEN)
        self.igralna_plosca.grid(row=1, column=0)
        self.narisi_polje()

        # Click event handler
        self.igralna_plosca.bind("<Button-1>", self.klik_na_plosco)


    def narisi_polje(self):
        # draw the lines
        self.igralna_plosca.create_line(self.width/3, (self.height/20), self.width/3, 19*(self.height/20))
        self.igralna_plosca.create_line(2*self.width/3, (self.height/20), 2*self.width/3, 19*(self.height/20))
        self.igralna_plosca.create_line(self.width/20, self.height/3, 19*(self.width/20), self.height/3)
        self.igralna_plosca.create_line(self.width/20, 2*self.height/3, 19*(self.width/20), 2*self.height/3)

    def narisi_figuro_O(self, i, j):
        self.igralna_plosca.create_oval((4+(i*20))*(self.width/60), (4+(j*20))*(self.height/60), (16+(i*20))*(self.width/60), (16+(j*20))*(self.height/60), width=self.debelina,outline=self.barvaIgralecO)

    def narisi_figuro_X(self,i, j):
        self.igralna_plosca.create_line((4+(i*20))*(self.width/60), (4+(j*20))*(self.height/60), (16+(i*20))*(self.width/60), (16+(j*20))*(self.height/60), width=self.debelina,fill=self.barvaIgralecX)
        self.igralna_plosca.create_line((4+(i*20))*(self.width/60), (16+(j*20))*(self.height/60), (16+(i*20))*(self.width/60), (4+(j*20))*(self.height/60), width=self.debelina,fill=self.barvaIgralecX)

    def ZacniIgro(self,igralec1,igralec2):
        self.ugasniIgralce()
        self.igralecO = igralec1
        self.igralecX = igralec2
        self.imeIgralecO = igralec1.ime
        self.imeIgralecX = igralec2.ime
        self.narisi_polje()
        self.igralna_plosca.delete(tkinter.ALL)
        self.narisi_polje()


        self.igra = Igra.Igra()
        self.igralecO.igraj()

        self.Siri.set("Na potezi je {0}".format(self.imeIgralecO))

        if self.player1 == "":
            self.player1 = self.imeIgralecO
            self.player2 = self.imeIgralecX


    def ugasniIgralce(self):
        if self.igralecO != None:
            self.igralecO.prekini()
            self.igralecX.prekini()

    def zaprriOkno(self,master):
        self.ugasniIgralce()
        master.destroy()

    def klik_na_plosco(self, event):
        i = int(event.x//(self.width/3))
        j = int(event.y//(self.height/3))
        assert i<3 or j<3, "To je neveljaven klik"
        if self.igra.naPotezi == self.igra.IGRALEC_O:
            self.igralecO.klik(i,j)
        if self.igra.naPotezi == self.igra.IGRALEC_X:
            self.igralecX.klik(i,j)

    def zmagovalnaCrta(self,kako):
        ((x1,y1),(x2,y2),(x3,y3)) = kako
        self.igralna_plosca.create_line((2*x1+1)*(self.width/6), (2*y1+1)*(self.height/6),(2*x3+1)*(self.width/6), (2*y3+1)*(self.height/6),width=2*self.debelina)

    def izvediPotezo(self,i,j):
        kdo = self.igra.naPotezi
        a = self.igra.igrajPotezo(i,j)
        if a == None:
            pass
            print("No spam pls")
        else:
            if kdo == self.igra.IGRALEC_O:
                self.narisi_figuro_O(i,j)
            elif kdo == self.igra.IGRALEC_X:
                self.narisi_figuro_X(i,j)
            kaj, kako = a
            if kaj == self.igra.NIKONEC:
                if self.igra.naPotezi == self.igra.IGRALEC_O:
                    self.Siri.set("Na potezi je {0}".format(self.imeIgralecO))
                    self.igralecO.igraj()
                else:
                    self.Siri.set("Na potezi je {0}".format(self.imeIgralecX))
                    self.igralecX.igraj()
            elif kaj == self.igra.NIHCENEZMAGA:
                self.Siri.set("Neodločeno ╭∩╮(Ο_Ο)╭∩╮")
            else:
                if kdo == self.igra.IGRALEC_X:
                    self.Siri.set("Zmagovalec je {0}".format(self.imeIgralecX))
                else:
                    self.Siri.set("Zmagovalec je {0}".format(self.imeIgralecO))
                self.zmagovalnaCrta(kako)

    #Menu window za novo igro
    def izbira_nove_igre(self):
        """Napravi okno, kjer si lahko izberemo nastavitve za novo igro, ter jo tako zacnemo"""

        def creategame(kateri):
            """Pomozna funkcija ki naredi novo igro"""
            if igralec1_clovek.get():
                igralec1 = Igralec.Igralec(self, ime1.get(), None)
            else:
                igralec1 = Racunalnik.Racunalnik(self,ime1.get(),None,int(var.get()))
            if igralec2_clovek.get():
                igralec2 = Igralec.Igralec(self,ime2.get(), None)
            else:
                igralec2 = Racunalnik.Racunalnik(self,ime2.get(),None,int(var2.get()))
            if kateri == 1:
                self.ZacniIgro(igralec1,igralec2)
            else:
                self.ZacniIgro(igralec2,igralec1)
            nov_game.destroy()


        #ustvari novo okno
        nov_game = tkinter.Toplevel()
        nov_game.grab_set()
        nov_game.title('Križci in krožci - nova igra')     #nastavi ime okna
        nov_game.resizable(width=False, height=False)

        for stolpec in range(4):
            nov_game.grid_columnconfigure(stolpec, minsize=100)

        tkinter.Label(nov_game, text='Nastavitve nove igre', font=('Times',20)).grid(column=0, row=0, columnspan=5)

        #nastavitve igralcev
        tkinter.Label(nov_game, text='Igralec 1', font=('Times',12)).grid(column=1, row=1)
        tkinter.Label(nov_game, text='Igralec 2', font=('Times',12)).grid(column=3, row=1)
        tkinter.Label(nov_game, text="Tip igralca:").grid(row=2, column=0, rowspan=2, sticky="E")
        tkinter.Label(nov_game, text="Tip igralca:").grid(row=2, column=2, rowspan=2, sticky="E")
        tkinter.Label(nov_game, text="Težavnost:").grid(row=5, column=0, rowspan=2, sticky="E")
        tkinter.Label(nov_game, text="Težavnost:").grid(row=5, column=2, rowspan=2, sticky="E")

        igralec1_clovek = tkinter.BooleanVar()
        igralec1_clovek.set(True)
        igralec2_clovek = tkinter.BooleanVar()
        igralec2_clovek.set(True)
        igralci = [("Človek", True, igralec1_clovek, 3, 1), ("Računalnik", False, igralec1_clovek, 4, 1),
                   ("Človek", True, igralec2_clovek, 3, 3), ("Računalnik", False, igralec2_clovek, 4, 3)]

        var = tkinter.StringVar(nov_game)
        var.set(2)
        option = tkinter.OptionMenu(nov_game, var, 1, 2)
        option.grid(row=5, column=1)

        var2 = tkinter.StringVar(nov_game)
        var2.set(2)
        option2 = tkinter.OptionMenu(nov_game, var2, 1, 2)
        option2.grid(row=5, column=3)

        for besedilo, vrednost, spremenljivka, vrstica, stolpec in igralci:
            tkinter.Radiobutton(nov_game, text=besedilo, variable=spremenljivka, value=vrednost, width=10, anchor="w")\
                .grid(row=vrstica, column=stolpec)

        tkinter.Label(nov_game, text="Ime igralca:").grid(row=7, column=0, sticky="E")
        tkinter.Label(nov_game, text="Ime igralca:").grid(row=7, column=2, sticky="E")

        ime1 = tkinter.Entry(nov_game, font=('Times', 12), width=10)
        ime1.grid(row=7, column=1)
        ime1.insert(0, self.player1)

        ime2 = tkinter.Entry(nov_game, font=('Times', 12), width=10)
        ime2.grid(row=7, column=3)
        ime2.insert(0, self.player2)

        GumbPreklic = tkinter.Button(nov_game, text="Začni Igralec 1", width=20, height=2, command=lambda: creategame(1))
        GumbPreklic.grid(row=8, column=0, columnspan=2) #, sticky=N+W+E+S)
        GumbZacni = tkinter.Button(nov_game, text="Zacni Igralec 2", width=20, height=2, command=lambda: creategame(2))
        GumbZacni.grid(row=8, column=2, columnspan=2) #, sticky=N+W+E+S)

    def okno_navodila(self):
        navodila_win = tkinter.Toplevel()
        navodila_win.grab_set()
        navodila_win.title('Križci in krožci - Navodila')     #nastavi ime okna
        navodila_win.resizable(width=False, height=False)

        napis_navodila = """Igro lahko igrata dva igralca, v tem primeru izberem »Tip igralca«
tako za igralca 1 kot za igralca 2 vrednost »Človek«. V tem primeru ne izbiramo težavnosti.
Vnesemo lahko tudi imeni obeh igralcev. Na koncu s klikom na enega izmed gumbov
»Začni Igralec 1« oziroma »Začni Igralec 2« določimo kdo začne igro.
Pri  igralcu 2  (enako velja za igralca 1) lahko izberem »Tip igralca«  vrednost »Računalnik«,
V tem primeru imamo na izbiro dve težavnosti, težavnost 1 pomeni, da računalnik naključno riše X
po igralnem oknu, če pa izberemo težavnost 2, računalnik igra optimalno.
Če začne igro računalnik, potrebuje za prvo potezo nekaj sekund.
"""
        navodila = tkinter.StringVar(navodila_win,value = napis_navodila)
        tkinter.Label(navodila_win, textvariable=navodila, font=("Calibri", 11)).grid(row=0, column=0)



if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Križci in krožci")
    aplikacija = Gui(root)
    IgralecO = Igralec.Igralec(aplikacija,"Žiga",None)
    IgralecX = Racunalnik.Racunalnik(aplikacija,"Luka",None,2)
    aplikacija.ZacniIgro(IgralecO,IgralecX)
    root.resizable(width=False, height=False)
    root.mainloop()
