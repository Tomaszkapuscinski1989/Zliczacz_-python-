from tkinter import *
from tkcalendar import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import babel.numbers
import datetime as dt
import os

import Menu
import workers
import work_2
import file
import filePDF
import history
import wykresy
import menager


font_m = ("Times", "14")
font_d = ("Times", "18")
kolor_bg1 = "#f7f8f9"
kolor_bg2 = "#ccd3de"
kolor_bg3 = "#3a4454"
kolor_text1 = "black"
kolor_text2 = "white"

class Main(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Program")
        self.geometry('800x200')
        self.minsize(800, 200)
        self.tk_setPalette(background="white")
        self.root = self
        self.nazwa_bazy = ""

        self.wykres1 = wykresy.Wykresy(self)

        w1= {'wykres': self.wykres1,
            'tabela': 'work_1' ,
            'rodzaj': "zwijanie"}
        w2= {'wykres': self.wykres1,
            'tabela': 'work_2' ,
            'rodzaj': "prasa"}

        self.work_1 = work_2.Work.from_dick(self,w1)
        self.work_2 = work_2.Work.from_dick(self,w2)
        self.workers = workers.Workers(self, w1['tabela'], w2['tabela'])
        self.file = file.Files()
        self.filePDF = filePDF.Files()
        self.history = history.History(self.root)

        Menu.menu_bar(self,
            1,
            self.nowa_baza,
            self.open_baza,
            self.workers.show_workers,
            self.workers.workers_add_rekord,
            self.workers.select_worker,
            self.workers.select_worker,
            self.work_1.show_work,
            self.work_1.add_work,
            self.work_1.add_column_work,
            self.work_1.select_work,
            self.work_1.select_work,
            self.work_2.show_work,
            self.work_2.add_work,
            self.work_2.add_column_work,
            self.work_2.select_work,
            self.work_2.select_work,
            self.file.print_to_txt,
            self.filePDF.print_to_pdf,
            self.history.show_history)

        self.zegarek1 = Label(self, text=0, fg=kolor_text1, font=font_d)
        self.zegarek2 = Label(self, text=0, fg=kolor_text1, font=font_d)
        self.zegarek1.pack(pady=10)
        self.zegarek2.pack()
        self.aktualny_czas()
        self.zegarek1.bind("<Button-1>", Main.calendar)

    def nowa_baza(self):

        self.nazwa_bazy = filedialog.asksaveasfilename(defaultextension="*.db", filetypes=(("db", "*.db"),))

        if self.nazwa_bazy:
            nazwa = self.nazwa_bazy.split("/")
            if os.path.exists(f"{nazwa[-1]}"):
               os.remove(f"{nazwa[-1]}")

            self.title(f"Program - {nazwa[-1]}")

            with menager.open_base(self.nazwa_bazy) as c:
                c.execute("""CREATE TABLE workers (
                    imie TEXT,
                    nazwisko TEXT,
                    telefon INTIGER DEFAULT 0
                    ) """)

                c.execute("""CREATE TABLE work_1 (
                    worker_id INTIGER PRIMARY KEY,
                    nazwisko TEXT,
                    Dzien_1 REAL DEFAULT 0
                    ) """)

                c.execute("""CREATE TABLE work_2 (
                    worker_id INTIGER PRIMARY KEY,
                    nazwisko TEXT,
                    Dzien_1 REAL DEFAULT 0
                    ) """)

                c.execute("""CREATE TABLE history (
                    start TEXT,
                    koniec TEXT DEFAULT "Sesja w toku"
                    ) """)
                messagebox.showinfo("info", "Baza utworzona pomyślnie")

            Menu.menu_bar(self,
                2,
                self.nowa_baza,
                self.open_baza,
                self.workers.show_workers,
                self.workers.workers_add_rekord,
                self.workers.select_worker,
                self.workers.select_worker,
                self.work_1.show_work,
                self.work_1.add_work,
                self.work_1.add_column_work,
                self.work_1.select_work,
                self.work_1.select_work,
                self.work_2.show_work,
                self.work_2.add_work,
                self.work_2.add_column_work,
                self.work_2.select_work,
                self.work_2.select_work,
                self.file.print_to_txt,
                self.filePDF.print_to_pdf,
                self.history.show_history)

            self.workers.nowa(self.nazwa_bazy)
            self.work_1.nowa(self.nazwa_bazy)
            self.work_2.nowa(self.nazwa_bazy)
            self.file.nowa(self.nazwa_bazy)
            self.filePDF.nowa(self.nazwa_bazy)
            self.history.nowa(self.nazwa_bazy)
            self.history.start_history()
            self.wykres1.nowa(self.nazwa_bazy)
            self.wykres1.wykres1()

    def open_baza(self):

        self.nazwa_bazy = filedialog.askopenfilename(filetypes=(("db", "*.db"),))

        if self.nazwa_bazy:

            nazwa=self.nazwa_bazy.split("/")
            self.root.title(f"Program - {nazwa[-1]}")

            Menu.menu_bar(self,
                2,
                self.nowa_baza,
                self.open_baza,
                self.workers.show_workers,
                self.workers.workers_add_rekord,
                self.workers.select_worker,
                self.workers.select_worker,
                self.work_1.show_work,
                self.work_1.add_work,
                self.work_1.add_column_work,
                self.work_1.select_work,
                self.work_1.select_work,
                self.work_2.show_work,
                self.work_2.add_work,
                self.work_2.add_column_work,
                self.work_2.select_work,
                self.work_2.select_work,
                self.file.print_to_txt,
                self.filePDF.print_to_pdf,
                self.history.show_history)

            self.workers.nowa(self.nazwa_bazy)
            self.work_1.nowa(self.nazwa_bazy)
            self.work_2.nowa(self.nazwa_bazy)
            self.file.nowa(self.nazwa_bazy)
            self.filePDF.nowa(self.nazwa_bazy)
            self.history.nowa(self.nazwa_bazy)
            self.history.start_history()
            self.wykres1.nowa(self.nazwa_bazy)
            self.wykres1.wykres1()

    def aktualny_czas(self):
        data = dt.datetime.now()
        self.zegarek1["text"] = data.strftime("%d-%m-%Y")
        self.zegarek2["text"] = data.strftime("%H:%M:%S")
        self.after(200, self.aktualny_czas)

    @staticmethod
    def calendar(e):
        window = Toplevel()
        window.geometry('300x300')
        window.title('Kalendarz')

        data = dt.datetime.now()
        day = data.day
        month = data.month
        year = data.year

        cal = Calendar(window, selectmode="day", day=day, month=month, year=year, headersforeground=kolor_text2, headersbackground=kolor_bg3, background=kolor_bg3, bordercolor=kolor_bg3)
        cal.pack(fill=BOTH, expand=True)
#________________________________________________________________________________________________


if __name__ == '__main__':

    start = Main()

    s = ttk.Style()
    s.configure('my.TButton', font=('Helvetica', 15))
    #s.map('my.TButton', relief=[('pressed', 'SUNKEN'), ('!pressed', 'rised')])
    #style.theme_use("default")
    s.configure("mystyle.Treeview",
        rowheight=25,
        fieldbackground=kolor_bg1
        )

    s.map('mystyle.Treeview',
        background=[('selected', 'blue')],
        foreground=[('selected',kolor_text2)])


    start.protocol("WM_DELETE_WINDOW", start.history.end_histry)
    start.mainloop()
