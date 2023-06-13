from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime as dt
import sqlite3 as sq

import Menu
import menager

font_m = ("Times", "14")
font_d = ("Times", "18")
kolor_bg1 = "#f7f8f9"
kolor_bg2 = "#ccd3de"
kolor_bg3 = "#3a4454"
kolor_text1 = "black"
kolor_text2 = "white"

class Work:

    def __init__(self, root, wykres, tabela, rodzaj):
        self.nazwa_bazy = ""
        self.Wykres = wykres
        self.tabela = tabela
        if self.tabela == "work_2":
            self.tabela2 = 'work_1'
            self.menu = 4
        else:
            self.tabela2 = 'work_2'
            self.menu = 2
        self.rodzaj = rodzaj
        self.root = root

    @classmethod
    def from_dick(cls,root, dick):
        return cls(root, dick['wykres'], dick['tabela'], dick['rodzaj'])

    def nowa(self,nazwa_bazy):
        self.nazwa_bazy = nazwa_bazy

    def normal(self):
        Menu.show_r.entryconfigure(self.menu, state='normal')
        self.window_1.destroy()

    def show_work(self):
        self.window_1 = Toplevel()
        self.window_1.title(f'Dane pracowników - {self.rodzaj}')
        self.window_1.geometry("1000x410")

        self.ramka = Frame(self.window_1)
        self.ramka.pack(pady=20, padx=30, fill=X)

        ods = ttk.Button(self.ramka, text="Odswierz", style='my.TButton')
        ods.pack(fill=X)

        ods.bind("<Button-1>", self.refresh)
        ods.bind("<Return>", self.refresh)

        self.ods1 = ttk.Button(self.ramka, text="1", style='my.TButton')
        self.ods1.pack(side=RIGHT, fill=X, expand=True)
        self.ods1.bind("<Button-1>", lambda event, x = self.tabela, y = self.rodzaj: self.Wykres.wykres2_w2(x, y))
        self.ods1.bind("<Return>", lambda event, x = self.tabela, y = self.rodzaj: self.Wykres.wykres2_w2(x, y))

        self.ods2 = ttk.Button(self.ramka, text="2", style='my.TButton')
        self.ods2.pack(side=RIGHT, fill=X, expand=True)
        self.ods2.bind("<Button-1>", lambda event, x = self.tabela, y = self.rodzaj: self.Wykres.wykres3_w2(x, y))
        self.ods2.bind("<Return>", lambda event, x = self.tabela, y = self.rodzaj: self.Wykres.wykres3_w2(x, y))


        self.ods3 = ttk.Button(self.ramka, text="3", style='my.TButton')
        self.ods3.pack(side=RIGHT, fill=X, expand=True)
        self.ods3.bind("<Button-1>", lambda event, x = self.tabela, y = self.rodzaj: self.Wykres.wykres4_w2(x, y))
        self.ods3.bind("<Return>", lambda event, x = self.tabela, y = self.rodzaj: self.Wykres.wykres4_w2(x, y))


        self.ods4 = ttk.Button(self.ramka, text=u"\u23EB", style='my.TButton')
        self.ods4.pack(side=RIGHT, fill=X, expand=True)
        self.ods4.bind("<Button-1>", lambda event, x = self.tabela, y = self.rodzaj: self.Wykres.wykres4_w2(x, y))
        self.ods4.bind("<Return>", lambda event, x = self.tabela, y = self.rodzaj: self.Wykres.wykres4_w2(x, y))

        Menu.show_r.entryconfigure(self.menu, state='disabled')

        self.window_1.protocol("WM_DELETE_WINDOW", self.normal)

        self.show_work_1()

    def show_work_1(self):

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(f"SELECT * FROM {self.tabela}")
            r = c.fetchone()
            c.execute(f"SELECT * FROM {self.tabela} ORDER BY worker_id")
            r2 = c.fetchall()
        try:
            z = ["Id", "Nazwisk"]
            for m in range(1, len(r[2:])+1):
                z.append(f"Wpis {m}")
            sumy_dzienne=[0.0 for i in range(len(r)-2)]
            z.append('Suma')

        except TypeError:
            self.ods1.configure(state='disabled')
            self.ods2.configure(state='disabled')
            self.ods3.configure(state='disabled')
            self.ods4.configure(state='disabled')
            blad= Label(self.window_1, font=font_m, text="Brak wpisów w bazie", bg = kolor_bg2, fg=kolor_text1)
            blad.pack(ipadx=10, ipady=10, fill=X, expand=True)

        else:
            self.tree_frame = Frame(self.window_1)
            self.tree_frame.pack(pady=20, padx=30, fill=X, expand=True)

            tree_scrolly = ttk.Scrollbar(self.tree_frame)
            tree_scrollx = ttk.Scrollbar(self.tree_frame, orient=HORIZONTAL)
            tree_scrollx.pack(side=BOTTOM, fill=X)
            tree_scrolly.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(self.tree_frame,style="mystyle.Treeview", selectmode='browse', yscrollcommand=tree_scrolly.set, xscrollcommand=tree_scrollx.set)
            my_tree.pack( fill=X, expand=True)

            my_tree.tag_configure('odd', background=kolor_bg1)
            my_tree.tag_configure('even', background=kolor_bg2)
            my_tree.tag_configure('suma', background=kolor_bg3)
            my_tree.tag_configure('suma_text', foreground=kolor_text2)

            tree_scrolly.config(command=my_tree.yview)
            tree_scrollx.config(command=my_tree.xview)

            my_tree['columns']= tuple(z)

            my_tree.column("#0", width=0, stretch=NO)
            my_tree.heading("#0", text="", anchor=E)

            my_tree.column(z[0], anchor=E, width=25)
            my_tree.heading(z[0], text=z[0], anchor=E)

            my_tree.column(z[1], anchor=E, width=140)
            my_tree.heading(z[1], text=z[1], anchor=E)

            for t in range(len(z)-3):
                my_tree.column(z[t+2], anchor=E, width=60)
                my_tree.heading(z[t+2], text=z[t+2], anchor=E)

            my_tree.column('Suma', anchor=E, width=60)
            my_tree.heading('Suma', text='Suma', anchor=E)

            for counter, value in enumerate(r2):
                sumy_dzienne = [sum(x) for x in zip(sumy_dzienne, value[2:])]
                #tablica liczoca ilość wykonana w poszczegolne dni

                całowita_ilosc=sum(value[2:])#calkowita ilosc wykonanana przez pracownika
                pst = list(value)
                pst.append(całowita_ilosc)#ilość wykonana w poszczegolne dni + całkowita ilosc
                if counter % 2 ==0:
                    my_tree.insert(parent='', index='end', iid=counter, text="", values=pst, tags = ('odd',))
                else:
                    my_tree.insert(parent='', index='end', iid=counter, text="", values=pst, tags = ('even',))
            h= ["", ""] + sumy_dzienne

            my_tree.insert(parent='', index='end', iid=counter+1, text="", values=h ,tags = ('suma','suma_text'))

    def refresh(self, event):
        for w in self.window_1.winfo_children()[1:]:
            w.destroy()

        self.show_work_1()

    def add_work(self):
        self.window_2 = Toplevel()
        self.window_2.title(f'Dodaj pracownika - {self.rodzaj}')

        imie_pracownika=Label(self.window_2, text="Numer pracownika")
        imie_pracownika.grid(row=0, column=0)

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("SELECT oid FROM workers")
            lista = c.fetchall()

        lista.insert(0, "Wybierz id")

        self.wybor_id= ttk.Combobox(self.window_2, font=font_m, value= lista)
        self.wybor_id.current(0)
        self.wybor_id.grid(row=0, column=1, padx= 10, pady=10)

        zapisz= ttk.Button(self.window_2, text="Zapisz", style='my.TButton')
        zapisz.grid(row=1, column=0, columnspan=2, sticky=W+E, padx= 10, pady=10)

        zapisz.bind("<Button-1>", self.add_work_1)
        zapisz.bind("<Return>", self.add_work_1)

    def add_work_1(self, event):
        with menager.open_base(self.nazwa_bazy) as c:
            c.execute("SELECT nazwisko FROM workers WHERE oid = :oid", {'oid': self.wybor_id.get()})
            r = c.fetchone()

        try:
            with menager.open_base(self.nazwa_bazy) as c:
                c.execute(f"INSERT INTO {self.tabela} (worker_id, nazwisko) VALUES (:id, :nazwisko)",
                {
                    'id' : self.wybor_id.get(),
                    'nazwisko': r[0]
                })
        except TypeError:
            self.window_2.destroy()
            messagebox.showerror("Błąd", "Nie wybrano pracownika")
        except sq.IntegrityError:
            self.window_2.destroy()
            messagebox.showerror("Błąd", "id juz w bazie")
        else:
            self.window_2.destroy()
            messagebox.showinfo("Info", "Pracownik Dodany")

    def add_column_work(self):
        """dodaje kolumne do tabel"""
        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(f"SELECT * FROM {self.tabela2}")
            w1 = c.fetchall()

            c.execute(f"SELECT * FROM {self.tabela}")
            w2 = c.fetchall()

            try:
                numer = f'Dzien_{len(w1[0])-1}'
                z1 = f"ALTER TABLE {self.tabela2} ADD COLUMN {numer} REAL DEFAULT 0"
                c.execute(z1)
                numer = f'Dzien_{len(w2[0])-1}'
                z2 = f"ALTER TABLE {self.tabela} ADD COLUMN {numer} REAL DEFAULT 0"
                c.execute(z2)
                messagebox.showinfo("Info", "Dodano kolumne")
            except IndexError:
                messagebox.showerror("Błąd", "Brak pracowników w bazie")

    def select_work(self, akc):
        self.window_3 = Toplevel()

        w = Label(self.window_3, font=font_m, text="Wybór id")
        w.grid(row=0, column=0, padx= 10, pady=10)

        with menager.open_base(self.nazwa_bazy) as c:
            c.execute(f"SELECT worker_id FROM {self.tabela}")
            lista = c.fetchall()

        lista.insert(0, "Wybierz id")

        self.wybor_id_1= ttk.Combobox(self.window_3, font=font_m, value= lista)
        self.wybor_id_1.current(0)
        self.wybor_id_1.grid(row=0, column=1, sticky=W+E, padx= 10, pady=10)

        if akc == 1:
            self.window_3.title(f'Edycja wpisu - {self.rodzaj}')

            try:
                with menager.open_base(self.nazwa_bazy) as c:
                    c.execute(f"SELECT * FROM {self.tabela}")
                    r = c.fetchall()
                lista2= [x for x in range(1,len(r[0][2:])+1)]
                lista2.insert(0, "Wybierz wpis")

            except IndexError:
                lista2= []
                lista2.insert(0, "Wybierz wpis")

            w = Label(self.window_3, text="Wybierz wpis", font=font_m,)
            w.grid(row=1, column=0)

            self.wybor_wpis= ttk.Combobox(self.window_3, font=font_m, value= lista2)
            self.wybor_wpis.current(0)
            self.wybor_wpis.grid(row=1, column=1, sticky=W+E, padx= 10, pady=10)

            k = ttk.Button(self.window_3, text="Wpis do edycji", style='my.TButton')
            k.grid(row=2, column=0, columnspan=7, sticky=W+E, padx= 10, pady=10)

            k.bind("<Button-1>", lambda event, ak = 1: self.edit_work(ak))
            k.bind("<Return>", lambda event, ak = 1: self.edit_work(ak))

        elif akc ==2:
            self.window_3.title(f'Usuń wpisu - {self.rodzaj}')

            k = ttk.Button(self.window_3, text="Wpis do usunięcia", style='my.TButton')
            k.grid(row=1, column=0, columnspan=7, sticky=W+E, padx= 10, pady=10)

            k.bind("<Button-1>", lambda event, ak = 2: self.edit_work(ak))
            k.bind("<Return>", lambda event, ak = 2: self.edit_work(ak))

    def edit_work(self, ak):

        if ak == 1:
            try:
                with menager.open_base(self.nazwa_bazy) as c:
                    c.execute(f"SELECT * FROM {self.tabela} where worker_id=:oid",{'oid': self.wybor_id_1.get()})
                    r = c.fetchone()

                numer = r[0]
                nazwisko = r[1]

                wpis = f"Wpis {self.wybor_wpis.get()}"
                wartosc = r[int(self.wybor_wpis.get()) + 1]

            except TypeError:
                messagebox.showerror("Błąd", "Nie wybrano pracownika")

            except ValueError:
                messagebox.showerror("Błąd", "Nie wybrano numeru wpisu")

            except:
                messagebox.showerror("Błąd", "Nie znany błąd")

            else:
                id_pracownika = Label(self.window_3, font=font_d, text="Id", bg = kolor_bg3, fg=kolor_text2)
                nazwisko_pracownika = Label(self.window_3, font=font_d, text="Nazwisko", bg = kolor_bg3, fg=kolor_text2)
                id_pracownika.grid(row=3, column=0, sticky=W+E)
                nazwisko_pracownika.grid(row=3, column=1, sticky=W+E)

                s = Label(self.window_3, text=numer, font=font_m, bg = kolor_bg2, fg=kolor_text1)
                s.grid(row=4, column=0, sticky=W+E)
                s1 = Label(self.window_3, text=nazwisko, font=font_m, bg = kolor_bg2, fg=kolor_text1)
                s1.grid(row=4, column=1, sticky=W+E)

                q1_l = Label(self.window_3, font=font_d, text=wpis, bg = kolor_bg3, fg=kolor_text2)
                q1_l.grid(row=3, column=3, sticky=W+E)
                q1 = Label(self.window_3, text=wartosc, font=font_m, bg = kolor_bg2, fg=kolor_text1)
                q1.grid(row=4, column=3, sticky=W+E)

                self.entry_1 = Entry(self.window_3, font=font_m, bg = kolor_bg1, fg=kolor_text1)
                self.entry_1.insert(0, wartosc)
                self.entry_1.grid(row=5, column=3, sticky=W+E, padx= 10, pady=10)

                zapisz= ttk.Button(self.window_3, text="Zapisz", style='my.TButton')
                zapisz.grid(row=6, column=0, columnspan=7, sticky=W+E, padx= 10, pady=10)

                zapisz.bind("<Button-1>", lambda event, ak = 3: self.edit_work(ak))
                zapisz.bind("<Return>", lambda event, ak = 3: self.edit_work(ak))

        elif ak == 2:
            if self.wybor_id_1.get() == "Wybierz id":
                messagebox.showerror("Błąd", "Wybierz pracownika  do usunięcia")

            else:
                try:
                    with menager.open_base(self.nazwa_bazy) as c:
                        c.execute(f"DELETE FROM {self.tabela} where worker_id=:oid",{'oid': self.wybor_id_1.get()})

                    self.window_3.destroy()
                    messagebox.showinfo("Info", "Usunięto wpis")

                except:
                    with menager.open_base(self.nazwa_bazy) as c:
                        c.execute(f"DELETE FROM {self.tabela} where worker_id=:oid",{'oid': self.wybor_id_1.get()})

                    self.window_3.destroy()
                    messagebox.showinfo("Info", "Usunięto wpis")

        elif ak == 3:

            k = self.wybor_id_1.get()
            t = self.wybor_wpis.get()
            dane_1 = self.entry_1.get()

            m = f"UPDATE {self.tabela} SET Dzien_{t}={dane_1} WHERE worker_id={k}"
            try:
                with menager.open_base(self.nazwa_bazy) as c:
                    c.execute(m)

            except sq.ProgrammingError:
                with menager.open_base(self.nazwa_bazy) as c:
                    c.execute(m)

            except sq.OperationalError:
                messagebox.showerror("Błąd", "Używaj liczb i kropki w zapisie dziesiętnym")

            except Exception:
                self.window_3.destroy()
                messagebox.showerror("Błąd", "Nieznany błąd")

            else:
                self.window_3.destroy()
                messagebox.showinfo("Info", "Wpis pomyślnie edytowano")
