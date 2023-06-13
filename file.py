from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import datetime as dt

import menager

font_m = ("Times", "14")
font_d = ("Times", "18")
kolor_bg1 = "#f7f8f9"
kolor_bg2 = "#ccd3de"
kolor_bg3 = "#3a4454"
kolor_text1 = "black"
kolor_text2 = "white"

class Files:

    def __init__(self):
        self.nazwa_bazy = ""

    def nowa(self,nazwa_bazy):
        self.nazwa_bazy = nazwa_bazy

    def print_to_txt(self):
        nazwa = self.nazwa_bazy.split("/")
        nazwa_pliku = nazwa[-1].split(".")

        w = dt.datetime.now()
        kik = w.strftime("%d-%m-%Y %H:%M:%S")

        k =f" Zestawienie pracowników oracowników dla pliku {nazwa[-1]}"
        t =f"\n\n Plik wygenerowano: {kik}\n\n"
        w ='\n-----------------------------------------------------------------------------------------'
        y ="\nZwijanie:\n-----------------------------------------------------------------------------------------'\n"


        with open(f"{nazwa_pliku[-2]}.txt",'w') as fd:
            fd.write(k)
            fd.write(t)
            fd.write(w)
            fd.write(y)
            with menager.open_base(self.nazwa_bazy) as c:
                c.execute("SELECT * FROM workers LEFT JOIN work_1 on workers.oid = work_1.worker_id")
                r = c.fetchall()

            for w in r:

                suma = 0
                lista = []
                for i in w[5:]:

                    suma += i
                    lista.append(str(i))
                fd.write(f'\nimię: {w[0]}')
                fd.write(f'\nnazwisko: {w[1]}')
                fd.write(f'\ntelefon: {w[2]}')
                fd.write(f"\nW sumie: {suma}")
                fd.write("\n")

            fd.write("\n-----------------------------------------------------------------------------------------'")
            fd.write("\nPrasa\n-----------------------------------------------------------------------------------------'\n")

            with menager.open_base(self.nazwa_bazy) as c:
                c.execute("SELECT * FROM workers LEFT JOIN work_2 on workers.oid = work_2.worker_id")
                r = c.fetchall()
            for w in r:

                suma = 0
                lista = []
                for i in w[5:]:
                    suma += i
                    lista.append(str(i))
                fd.write(f'\nimię: {w[0]}')
                fd.write(f'\nnazwisko: {w[1]}')
                fd.write(f'\ntelefon: {w[2]}')

                fd.write(f"\nW sumie: {suma}")
                fd.write("\n")

        messagebox.showinfo("Info", "Pomyślnie zapisano do pliku tekstowego")




