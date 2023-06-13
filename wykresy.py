from matplotlib import pyplot as plt
import numpy as np

from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import menager

#style.use("fivethirtyeight")

font_m = ("Times", "14")
font_d = ("Times", "18")
kolor_bg1 = "#f7f8f9"
kolor_bg2 = "#ccd3de"
kolor_bg3 = "#3a4454"
kolor_text1 = "black"
kolor_text2 = "white"

class Wykresy():

    def __init__(self, root):
        self.nazwa_bazy = ""
        self.root = root
        style.use("fivethirtyeight")

    def nowa(self,nazwa_bazy):
        self.nazwa_bazy = nazwa_bazy

    def wykres1(self):
        self.root.geometry('800x670')
        self.root.minsize(800, 670)

        #print(plt.style.available)

        wynik1 = []
        liczba_dni1 = []

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("SELECT * FROM work_1")
            zwijanie = c.fetchone()

        try:
            for z in range(1, len(zwijanie) - 1 ):
                with menager.open_base(self.nazwa_bazy) as c:
                    c.execute(f"SELECT SUM(Dzien_{z}) FROM work_1")
                    r1 = c.fetchall()
                wynik1.append(r1[0][0])
                liczba_dni1.append(z)

            x = np.arange(1, len(liczba_dni1) + 1)
            width = 0.40

            wynik2 = []
            liczba_dni2 = []

            with menager.open_base(self.nazwa_bazy) as c:
                c.execute("SELECT * FROM work_2")
                prasa = c.fetchone()

            for z in range(1, len(prasa) - 1 ):
                with menager.open_base(self.nazwa_bazy) as c:
                    c.execute(f"SELECT SUM(Dzien_{z}) FROM work_2")
                    r3 = c.fetchall()
                wynik2.append(r3[0][0])
                liczba_dni2.append(z)

        except TypeError:
            ods = ttk.Button(self.root, text="Odswierz", style='my.TButton', command=self.refresh)
            ods.pack(fill=X, padx= 10, pady=10)

            blad = Label(self.root, text="Brak danych", font=('Helvetica', 18))
            blad.pack(pady=20)
            blad2 = Label(self.root, text="Aby zobaczyć wykres\ndodaj pracowników do obu baz", font=('Helvetica', 15))
            blad2.pack()

        else:

            self.fig, self.ax = plt.subplots()
            #self.fig(figsize=(10,6))
            self.ax.bar(x + (width/2), wynik1, width=width, label="Zwijanie")
            self.ax.bar(x - (width/2), wynik2, width=width, label="Prasa")

            self.ax.legend()
            #plt.grid(True)
            self.fig.autofmt_xdate()

            self.ax.set_xticks(ticks=x)
            self.ax.set_xticklabels(labels=liczba_dni1)

            self.ax.set_title("Zestawienie")
            self.ax.set_xlabel("ilość dni")
            self.ax.set_ylabel("ilość")

            self.fig.tight_layout()

            ods = ttk.Button(self.root, text="Odswierz", style='my.TButton', command=self.refresh)
            ods.pack(fill=X, padx= 10, pady=10)

            c = FigureCanvasTkAgg(self.fig, self.root)
            c.draw()
            c.get_tk_widget().pack(fill=BOTH, expand=True)

            t = NavigationToolbar2Tk(c, self.root)
            t.update()
            c._tkcanvas.pack()

    def refresh(self):
        for w in self.root.winfo_children()[3:]:
            w.destroy()

        self.wykres1()

    def wykres2_w2(self, tabela, rodzaj):
        self.w4 = Toplevel()
        self.w4.title(f'Zestawienie pracownika - {rodzaj}')
        #self.w4.geometry('600x200')

        r1 = Frame(self.w4)
        r1.pack()

        s="Ilość zwiniety pierścieni w ujeciu dziennym dla konkretnego pracownika"
        Label(r1, font=font_m, fg=kolor_text1, text=s).grid(row=0, column=0, columnspan=17, sticky=W+E, padx= 10, pady=10)
        z="Wybierz id praciwnika"
        Label(r1, font=font_m, fg=kolor_text1, text=z).grid(row=1, column=0, sticky=W+E, padx= 10, pady=10)

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(f"SELECT worker_id FROM {tabela}")
            lista = c.fetchall()

        lista.insert(0, "Wybierz id")

        self.id_2= ttk.Combobox(r1, font=font_m, value=lista)
        self.id_2.current(0)
        self.id_2.grid(row=1, column=1,  sticky=W+E, padx= 10, pady=10)

        ods = ttk.Button(r1, text="Wyświetl", style='my.TButton', command=lambda: self.wykres2_w2_1(tabela, rodzaj))
        ods.grid(row=2, column=0, columnspan=17, sticky=W+E, padx= 10, pady=10)


    def wykres2_w2_1(self, tabela, rodzaj):
        #self.w4.geometry('600x670')

        for w in self.w4.winfo_children()[1:]:
            w.destroy()

        wynik1 = []


        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(f" SELECT * FROM {tabela} WHERE worker_id={self.id_2.get()}")
            zwijanie = c.fetchone()


        try:
            wynik1 = zwijanie[2:]

        except:
            blad = Label(self.w4, text="Brak danych", font=('Helvetica', 18))
            blad.pack(pady=20)
            blad2 = Label(self.w4, text="Aby zobaczyć wykres\ndodaj pracowników tabel", font=('Helvetica', 15))
            blad2.pack()

        else:
            x = [x for x in range(1, len(zwijanie[2:]) + 1 )]

            self.fig, self.ax = plt.subplots()

            self.ax.bar(x, wynik1)

            self.ax.set_xticks(ticks=x)
            self.ax.set_xticklabels(labels=x)

            self.ax.set_title("Zestawienie")
            self.ax.set_xlabel("ilość dni")
            self.ax.set_ylabel("ilość")

            self.fig.tight_layout()

            c = FigureCanvasTkAgg(self.fig, self.w4)
            c.draw()
            c.get_tk_widget().pack(fill=BOTH, expand=True)

            t = NavigationToolbar2Tk(c, self.w4)
            t.update()
            c._tkcanvas.pack()

    def wykres3_w2(self, tabela, rodzaj):
        self.w5 = Toplevel()
        self.w5.title(f'Dzienne zestawienie - {rodzaj}')
        self.w5.geometry('600x200')

        r1 = Frame(self.w5)
        r1.pack()

        s="Zestawienie dzienne - wykres kołowy"
        Label(r1, font=font_m, fg=kolor_text1, text=s).grid(row=0, column=0, columnspan=17, sticky=W+E, padx= 10, pady=10)
        z="Wybierz dzień"
        Label(r1, font=font_m, fg=kolor_text1, text=z).grid(row=1, column=0, sticky=W+E, padx= 10, pady=10)

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(f"SELECT * FROM {tabela} ")
            dni = c.fetchall()

        try:
            lista =[x for x in range(1, len(dni[0])-1)]
        except IndexError:
            lista = []

        lista.insert(0, "Wybierz dzień")

        self.day_3= ttk.Combobox(r1, font=font_m, value= lista)
        self.day_3.current(0)
        self.day_3.grid(row=1, column=1,  sticky=W+E, padx= 10, pady=10)

        ods = ttk.Button(r1, text="Wyświetl", style='my.TButton', command=lambda: self.wykres3_w2_1(tabela, rodzaj))
        ods.grid(row=2, column=0, columnspan=17, sticky=W+E, padx= 10, pady=10)

    def wykres3_w2_1(self, tabela, rodzaj):

        self.w5.geometry('600x670')

        for w in self.w5.winfo_children()[1:]:
            w.destroy()

        wynik1 = []
        try:
            m =f" SELECT Dzien_{self.day_3.get()} FROM {tabela} order by worker_id"

            with menager.open_base(self.nazwa_bazy) as c:
                c.execute(m)
                zwijanie = c.fetchall()
                c.execute(f"SELECT worker_id FROM {tabela} ORDER BY worker_id")
                ety2 = c.fetchall()

            wynik1 = [x[0] for x in zwijanie]
            ety =[str(x[0]) for x in ety2]
            wynik5 = [h for h in zip (wynik1, ety) if h[0] != 0]
            labels = [w[1] for w in wynik5]
            lis = [w[0] for w in wynik5]

        except:
            blad = Label(self.w5, text="Brak danych", font=('Helvetica', 18))
            blad.pack(pady=20)
            blad2 = Label(self.w5, text="Aby zobaczyć wykres\ndodaj pracowników do obu baz", font=('Helvetica', 15))
            blad2.pack()

        else:

            self.fig, self.ax = plt.subplots()

            self.ax.pie(lis, labels = labels, shadow= True, autopct="%1.1f%%")

            self.ax.set_title("Zestawienie")

            self.fig.tight_layout()

            c = FigureCanvasTkAgg(self.fig, self.w5)
            c.draw()
            c.get_tk_widget().pack(fill=BOTH, expand=True)

            t = NavigationToolbar2Tk(c, self.w5)
            t.update()
            c._tkcanvas.pack()

    def wykres4_w2(self, tabela, rodzaj):
        self.w6 = Toplevel()
        self.w6.title(f'Dzienne zestawienie - {rodzaj}')
        self.w6.geometry('600x200')

        r1 = Frame(self.w6)
        r1.pack()

        s="Zestawienie dzienne - wykres słupkowy"
        Label(r1, font=font_m, fg=kolor_text1, text=s).grid(row=0, column=0, columnspan=17, sticky=W+E, padx= 10, pady=10)
        z="Wybierz dzień"
        Label(r1, font=font_m, fg=kolor_text1, text=z).grid(row=1, column=0, sticky=W+E, padx= 10, pady=10)

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(f"SELECT * FROM {tabela}")
            dni = c.fetchall()

        try:
            lista =[x for x in range(1, len(dni[0])-1)]
        except IndexError:
            lista = []

        lista.insert(0, "Wybierz dzień")
        self.day_4= ttk.Combobox(r1, font=font_m, value= lista)
        self.day_4.current(0)
        self.day_4.grid(row=1, column=1,  sticky=W+E, padx= 10, pady=10)

        ods = ttk.Button(r1, text="Wyświetl", style='my.TButton', command=lambda: self.wykres4_w2_1(tabela, rodzaj))
        ods.grid(row=2, column=0, columnspan=17, sticky=W+E, padx= 10, pady=10)

    def wykres4_w2_1(self, tabela, rodzaj):
        self.w6.geometry('600x670')

        for w in self.w6.winfo_children()[1:]:
            w.destroy()

        wynik1 = []

        try:
            m =f" SELECT Dzien_{self.day_4.get()} FROM {tabela} order by worker_id"

            with menager.open_base(self.nazwa_bazy) as c:
                c.execute(m)
                zwijanie = c.fetchall()
                c.execute(f"SELECT worker_id FROM {tabela} ORDER BY worker_id")
                ety2 = c.fetchall()

            wynik1 = [x[0] for x in zwijanie]
            ety =[str(x[0]) for x in ety2]
            wynik5 = [h for h in zip (wynik1, ety) if h[0] != 0]
            labels = [w[1] for w in wynik5]
            lis = [w[0] for w in wynik5]

        except:
            blad = Label(self.w6, text="Brak danych", font=('Helvetica', 18))
            blad.pack(pady=20)
            blad2 = Label(self.w6, text="Aby zobaczyć wykres\ndodaj pracowników do obu baz", font=('Helvetica', 15))
            blad2.pack()

        else:
            self.fig, self.ax = plt.subplots()

            self.ax.bar(labels, lis)

            self.ax.set_xticks(ticks=labels)
            self.ax.set_xticklabels(labels=labels)

            self.ax.set_title("Zestawienie")
            self.ax.set_xlabel("Indeks")
            self.ax.set_ylabel("Ilość")

            self.fig.tight_layout()

            c = FigureCanvasTkAgg(self.fig, self.w6)
            c.draw()
            c.get_tk_widget().pack(fill=BOTH, expand=True)

            t = NavigationToolbar2Tk(c, self.w6)
            t.update()
            c._tkcanvas.pack()








