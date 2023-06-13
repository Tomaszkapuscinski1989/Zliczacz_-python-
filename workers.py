from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime as dt

import Menu
import menager

font_m = ("Times", 14)
font_d = ("Times", 18)
kolor_bg1 = "#f7f8f9"
kolor_bg2 = "#ccd3de"
kolor_bg3 = "#3a4454"
kolor_text1 = "black"
kolor_text2 = "white"

class Workers:
    """klasa do zaarzadzania danymi przcowników"""

    def __init__(self, root, *args):
        """inicjalizacja zmiennych"""
        self.nazwa_bazy = ""
        self.root = root
        self.k1 = [arg for arg in args]

    def nowa(self, nazwa_bazy):
        """ przechwycenie nazwy bazy danych """
        self.nazwa_bazy = nazwa_bazy

    def menu(self):
        """ powrot menu do normalnego stanu po zamknięciu okna z podgladem pracownikow """
        Menu.show_r.entryconfigure(0, state='normal')
        #self.root.attributes('-alpha', 1)
        self.workers_window_1.destroy()

    def show_workers(self):
        """ definicja i otwarcie okana podgladu pracowników """
        self.workers_window_1 = Toplevel()
        self.workers_window_1.title('Dane pracowników')

        ods = ttk.Button(self.workers_window_1, text="Odswierz", style='my.TButton')
        ods.grid(row=0, column=0, columnspan=2, sticky=W+E, padx= 10, pady=10)

        ods.bind("<Button-1>", self.refresh)
        ods.bind("<Return>", self.refresh)

        #wysłaczenie opcji otwarcia okna podgladu pracowników
        Menu.show_r.entryconfigure(0, state='disabled')

        #definicja zachowania po naciśnęciu krzyzyka
        self.workers_window_1.protocol("WM_DELETE_WINDOW", self.menu)

        self.show_workers_1()

    def show_workers_1(self):
        """wyswietlenie zawartosci okana podgladu pracownikow"""

        #dodanie pola tekstowego z paskiem przewijania
        self.frame_1 = Frame(self.workers_window_1)

        self.yScroll = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
        self.yScroll.pack(side=RIGHT,fill=Y)

        self.workers_list = Listbox(self.frame_1, yscrollcommand=self.yScroll.set)
        self.frame_1.grid(row=1, column=0, padx=20, pady=20)
        self.workers_list.pack()

        self.yScroll.config(command= self.workers_list.yview)

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("SELECT *, oid FROM workers")
            r = c.fetchall()

        for w in r:
            k =f"{w[0]} {w[1]}"
            self.workers_list.insert(END, k)

        self.workers_list.config(activestyle='none', font=font_m)

        self.workers_list.bind("<Double-Button-1>", self.show_worker)

        # wyświetlanie pol na daane pracownika
        self.frame_2 = Frame(self.workers_window_1)
        self.frame_2.grid(row=1, column=1, sticky=S+N)

        id_lable = Label(self.frame_2, text="Id:", anchor=E)
        id_lable.grid(row=0, column=0, sticky=W+E)
        self.id_text = Label(self.frame_2, text="NaN", anchor=W)
        self.id_text.grid(row=0, column=1, sticky=W+E, padx=10)

        name_lable = Label(self.frame_2, text="Imię:", anchor=E)
        name_lable.grid(row=1, column=0, sticky=W+E)
        self.name = Label(self.frame_2, text="NaN", anchor=W)
        self.name.grid(row=1, column=1, sticky=W+E, padx=10)

        last_lable = Label(self.frame_2, text="Nazwisko:", anchor=E)
        last_lable.grid(row=2, column=0, sticky=W+E)
        self.last = Label(self.frame_2, text="NaN", anchor=W)
        self.last.grid(row=2, column=1, sticky=W+E, padx=10)

        phone_lable = Label(self.frame_2, text="Telefon:", anchor=E)
        phone_lable.grid(row=3, column=0, sticky=W+E)
        self.phone = Label(self.frame_2, text="NaN", anchor=W)
        self.phone.grid(row=3, column=1, sticky=W+E, padx=10)

    def show_worker(self, event):
        """wyświetlanie szcczegołow o wskazanym pracowniku"""
        index = self.workers_list.index(ANCHOR)

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("select *, oid FROM workers")
            r = c.fetchall()

        self.id_text.config(text=r[index][-1])
        self.name.config(text=r[index][0])
        self.last.config(text=r[index][1])
        self.phone.config(text=r[index][2])

    def refresh(self, event):
        """odswierzanie danych """
        for w in self.frame_1.winfo_children():
            w.destroy()
        for k in self.frame_2.winfo_children():
            k.destroy()
        self.show_workers_1()

    def workers_add_rekord(self):
        """tworzy okno do wpisywana danych o nowym pracowniku"""
        self.workers_window_2 = Toplevel()
        self.workers_window_2.title('Dodaj pracownika')

        imie_pracownika=Label(self.workers_window_2, text="Imię Pracownika", font=font_m)
        imie_pracownika.grid(row=0, column=0)
        nazwisko_pracownika=Label(self.workers_window_2, text="Nazwisko Pracownika", font=font_m)
        nazwisko_pracownika.grid(row=1, column=0)
        telefon_pracownika=Label(self.workers_window_2,text="Numer trlefonu", font=font_m)
        telefon_pracownika.grid(row=2, column=0)

        self.imie_pracownika_okno_2_pracownik=Entry(self.workers_window_2, font=font_m)
        self.imie_pracownika_okno_2_pracownik.grid(row=0, column=1, padx=10, pady=10)
        self.nazwisko_pracownika_okno_2_pracownik=Entry(self.workers_window_2, font=font_m)
        self.nazwisko_pracownika_okno_2_pracownik.grid(row=1, column=1, padx=10)
        self.telefon_pracownika_okno_2_pracownik=Entry(self.workers_window_2, font=font_m)
        self.telefon_pracownika_okno_2_pracownik.grid(row=2, column=1, padx=10, pady=10)

        zapisz=ttk.Button(self.workers_window_2, style='my.TButton', text="Zapisz")
        zapisz.grid(row=3, column=0, columnspan=3, sticky=W+E, padx= 10, pady=10)

        zapisz.bind("<Button-1>", self.workers_add_worker)
        zapisz.bind("<Return>", self.workers_add_worker)

    def workers_add_worker(self, event):
        """dodawanie wpisu o pracowniku do bazy"""
        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(" INSERT INTO workers VALUES (:imie, :nazwisko, :telefon)",
                {
                    'imie' : self.imie_pracownika_okno_2_pracownik.get(),
                    'nazwisko': self.nazwisko_pracownika_okno_2_pracownik.get(),
                    'telefon': self.telefon_pracownika_okno_2_pracownik.get()
                })

        self.workers_window_2.destroy()
        messagebox.showinfo("Info", "Dodano pracownika")

    def select_worker(self, akc):
        """wybor pracownika do edytowania/usuniecia"""
        self.workers_window_3 = Toplevel()
        self.workers_window_3.title('Wybierz pracownika o danym numerze')

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("SELECT oid FROM workers")
            lista = c.fetchall()

        lista.insert(0, "Wybierz id")

        w = Label(self.workers_window_3, font=font_m, text="Numer Pracownika")
        w.grid(row=0, column=0, padx= 10, pady=10)
        self.wybor_id_pracownik= ttk.Combobox(self.workers_window_3, value= lista, font=font_m)
        self.wybor_id_pracownik.current(0)
        self.wybor_id_pracownik.grid(row=0, column=1, padx= 10, pady=10)

        if akc == 1:
            k = ttk.Button(self.workers_window_3, text="Wpis do edycji", style='my.TButton')
            k.grid(row=1, column=0, columnspan=2, sticky=W+E, padx= 10, pady=10)

            k.bind("<Button-1>", self.select_worker_1)
            k.bind("<Return>", self.select_worker_1)

        elif akc == 2:
            k = ttk.Button(self.workers_window_3, text="Usuń wpis", style='my.TButton')
            k.grid(row=1, column=0, columnspan=7, sticky=W+E, padx= 10, pady=10)

            k.bind("<Button-1>", self.delete_worker)
            k.bind("<Return>", self.delete_worker)

    def select_worker_1(self, event):
        """wyswietla dane o edytowanym pracowniku"""
        i = self.wybor_id_pracownik.get()

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("SELECT * FROM workers WHERE oid=:wyb", {"wyb":i})
            r = c.fetchone()

        try:
            imie = r[0]
            nazwisko = r[1]
            telefon = r[2]

        except TypeError:
            messagebox.showerror("Błąd", "Nie wybrano pracownika")

        else:
            imie_pracownika=Label(self.workers_window_3, text="Imię Pracownika", font=font_m)
            imie_pracownika.grid(row=3, column=0, padx= 10, pady=10)
            nazwisko_pracownika=Label(self.workers_window_3, text="Nazwisko Pracownika", font=font_m)
            nazwisko_pracownika.grid(row=4, column=0, padx= 10, pady=10)
            telefon_pracownika=Label(self.workers_window_3,text="Numer trlefonu", font=font_m)
            telefon_pracownika.grid(row=5, column=0, padx= 10, pady=10)

            self.imie_pracownika_okno_3=Entry(self.workers_window_3, font=font_m)
            self.imie_pracownika_okno_3.grid(row=3, column=1, padx= 10, pady=10)
            self.nazwisko_pracownika_okno_3=Entry(self.workers_window_3, font=font_m)
            self.nazwisko_pracownika_okno_3.grid(row=4, column=1, padx= 10, pady=10)
            self.telefon_pracownika_okno_3=Entry(self.workers_window_3, font=font_m)
            self.telefon_pracownika_okno_3.grid(row=5, column=1, padx= 10, pady=10)

            self.imie_pracownika_okno_3.insert(0, imie)
            self.nazwisko_pracownika_okno_3.insert(0, nazwisko)
            self.telefon_pracownika_okno_3.insert(0, telefon)

            zapisz=ttk.Button(self.workers_window_3, text="Zapisz", style='my.TButton', command=self.edit_worker)
            zapisz.grid(row=6, column=0, columnspan=3, sticky=W+E, padx= 10, pady=10)

            zapisz.bind("<Button-1>", self.edit_worker)
            zapisz.bind("<Return>", self.edit_worker)

    def edit_worker(self, event):
        """edytowanie wpisu"""
        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("UPDATE workers SET imie=:imie, nazwisko=:nazwisko, telefon=:telefon WHERE oid=:oid",
                {
                'imie':self.imie_pracownika_okno_3.get(),
                'nazwisko':self.nazwisko_pracownika_okno_3.get(),
                'telefon':self.telefon_pracownika_okno_3.get(),
                'oid': self.wybor_id_pracownik.get()
                })
            c.execute("UPDATE work_1 SET nazwisko=:nazwisko WHERE worker_id=:oid",
                {
                'nazwisko':self.nazwisko_pracownika_okno_3.get(),
                'oid': self.wybor_id_pracownik.get()
                })
            c.execute("UPDATE work_2 SET nazwisko=:nazwisko WHERE worker_id=:oid",
                {
                'nazwisko':self.nazwisko_pracownika_okno_3.get(),
                'oid': self.wybor_id_pracownik.get()
                })
        self.workers_window_3.destroy()
        messagebox.showinfo("info", "Wpis pomyślnie edytowano")

    def delete_worker(self, event):
        """usuniecie pracowika z bazy pracownika"""
        if self.wybor_id_pracownik.get() == "Wybierz id":
            messagebox.showerror("Błąd", "Wybierz pracownika  do usunięcia")

        else:
            with menager.open_base(self.nazwa_bazy) as c:
                c.execute("DELETE FROM workers where oid=:oid",{'oid': self.wybor_id_pracownik.get()})
                for w in self.k1:
                    c.execute(f"DELETE FROM {w} where worker_id={self.wybor_id_pracownik.get()}")


            self.workers_window_3.destroy()
            messagebox.showinfo("info", "Usunięto pracownik")
















