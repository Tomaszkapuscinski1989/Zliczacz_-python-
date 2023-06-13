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

class History:
    """ klasa otpowiedzialna za kontrole czasu trwania sesji"""

    def __init__(self, root):
        """ inicjalizacja zmiennych i przechwycenie głownego okna"""
        self.nazwa_bazy = ""
        self.data_start = ""
        self.root = root

    def nowa(self,nazwa_bazy):
        """ przechwycenie nazwy bazy danych """
        self.nazwa_bazy = nazwa_bazy

    def start_history(self):
        """wpisuje date startu sesji do bazy danych """
        data = dt.datetime.now()

        self.data_start = data.strftime("%H:%M:%S %d-%m-%Y")
        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(" INSERT INTO history (start) VALUES (:id)",
                {
                    'id' : self.data_start
                })


    def end_histry(self):
        """wpisuje date końca sesji do bazy"""
        data = dt.datetime.now()
        data_end = data.strftime("%H:%M:%S %d-%m-%Y")
        try:
            with menager.open_base(self.nazwa_bazy) as c:
                c.execute(" UPDATE history SET koniec=:koniec WHERE start=:start",
                    {
                        'koniec' : data_end,
                        'start': self.data_start
                    })
        except:
            pass

        self.root.quit()

    def show_history(self):
        """wyswietla okono z poprzednimi wpisami o czasie sesji"""
        self.okno1 = Toplevel()
        self.okno1.title('Historia zmian')
        self.okno1.geometry('510x600')
        self.okno1.minsize(510, 600)
        self.okno1.maxsize(510, 600)

        #dodanie paska przewijania do całej ramki

        ramka1 = Frame(self.okno1)
        ramka1.pack(fill=BOTH, expand=1)

        canvas = Canvas(ramka1)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scroll = ttk.Scrollbar(ramka1, orient=VERTICAL, command=canvas.yview)
        my_scroll.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=my_scroll.set)
        canvas.bind('<Configure>', lambda e:  canvas.configure(scrollregion = canvas.bbox("all")))

        ramka2 = Frame(canvas)

        canvas.create_window((0,0) , window=ramka2, anchor="nw" )

        #zawartoś ramki

        id_s = Label(ramka2, font=font_d, bg = kolor_bg3, fg=kolor_text2, text="Id")
        start_s = Label(ramka2, font=font_d, bg = kolor_bg3, fg=kolor_text2, text="Początek sesji")
        end_s = Label(ramka2, font=font_d, bg = kolor_bg3, fg=kolor_text2, text="Koniec sesji")
        id_s.grid(row=2, column=0, sticky=W+E, ipadx=10)
        start_s.grid(row=2, column=1, sticky=W+E, ipadx=30)
        end_s.grid(row=2, column=2, sticky=W+E, ipadx=30)

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("select *, oid FROM history")
            r = c.fetchall()

        licznik = 2
        for wynik in r:
            if licznik % 2 == 0:
                id_s = Label(ramka2, font=font_m, bg = kolor_bg1, fg=kolor_text1, text=wynik[-1])
                start_s = Label(ramka2, font=font_m, bg = kolor_bg1, fg=kolor_text1, text=wynik[0])
                end_s = Label(ramka2, font=font_m, bg = kolor_bg1, fg=kolor_text1, text=wynik[1])

            else:
                id_s = Label(ramka2, font=font_m, bg = kolor_bg2, fg=kolor_text1, text=wynik[-1])
                start_s = Label(ramka2, font=font_m, bg = kolor_bg2, fg=kolor_text1, text=wynik[0])
                end_s = Label(ramka2, font=font_m, bg = kolor_bg2, fg=kolor_text1, text=wynik[1])

            licznik += 1
            id_s.grid(row=licznik + 1, column=0, sticky=W+E)
            start_s.grid(row=licznik + 1, column=1, sticky=W+E)
            end_s.grid(row=licznik + 1, column=2, sticky=W+E)
