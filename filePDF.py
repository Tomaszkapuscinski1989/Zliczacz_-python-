from reportlab.pdfgen.canvas import Canvas as C
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.platypus import PageBreak
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import datetime as dt
import sqlite3 as sq

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

    def print_to_pdf(self):
        nazwa = self.nazwa_bazy.split("/")
        nazwa_pliku = nazwa[-1].split(".")

        try:
            with menager.open_base(self.nazwa_bazy) as c:
                m = "SELECT * FROM workers LEFT JOIN work_1 on workers.oid = work_1.worker_id"
                c.execute(m)
                r = c.fetchall()
            elements = []

            text1 = f"Zestawienie pracowników oracowników dla pliku {nazwa[-1]}"
            tytul = Table([[text1]])

            text2= "Plik wygenerowano:"
            w = dt.datetime.now()
            kik = w.strftime("%d-%m-%Y %H:%M:%S")
            text3 = kik
            czas = Table([[text2, text3]])

            text4 = "Zwijanie:"
            work_1 = Table([[text4]])

            data = [("Id", "Imie pracownika", "Nazwisko pracownika", "Telefon", "Suma")]

            maintable = Table([[tytul],[czas],[work_1]])
            elements.append(maintable)

            for w in r:
                try:
                    lista = []
                    lista.append(w[3])
                    lista.append(w[0])
                    lista.append(w[1])
                    lista.append(w[2])
                    suma = 0
                    for i in w[5:]:
                        suma += i
                    lista.append(suma)
                    data.append(lista)
                except:
                    pass

            tablee = Table(data)
            elements.append(tablee)


            elements.append(PageBreak())

            with menager.open_base(self.nazwa_bazy) as c:
                m = "SELECT * FROM workers LEFT JOIN work_2 on workers.oid = work_2.worker_id"
                c.execute(m)
                d = c.fetchall()

            text4 = "Prasa:"
            work_2 = Table([[text4]])

            data2 = [("Id", "Imie pracownika", "Nazwisko pracownika", "Telefon", "Suma")]

            maintable2 = Table([[tytul],[czas],[work_2]])
            elements.append(maintable2)

            for w in d:
                try:
                    lista = []
                    lista.append(w[3])
                    lista.append(w[0])
                    lista.append(w[1])
                    lista.append(w[2])
                    suma = 0
                    for i in w[5:]:
                        suma += i
                    lista.append(suma)
                    data2.append(lista)
                except:
                    pass

            table2 = Table(data2)

            elements.append(table2)

            pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

            tytulStyle = TableStyle([
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTSIZE', (0,0), (-1,-1), 18),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Oblique'),
                ('TOPPADDING',(0,0),(-1,-1), 0),
                ('BOTTOMPADDING',(0,0),(-1,-1), 5),

            ])
            tytul.setStyle(tytulStyle)

            czasStyle = TableStyle([
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Oblique'),
                ('TOPPADDING',(0,0),(-1,-1), 2),
                ('BOTTOMPADDING',(0,0),(-1,-1), 2),

            ])
            czas.setStyle(czasStyle)

            work_1Style = TableStyle([
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTSIZE', (0,0), (-1,-1), 14),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Oblique'),
                ('TOPPADDING',(0,0),(-1,-1), 3),
                ('BOTTOMPADDING',(0,0),(-1,-1), 3),

            ])
            work_1.setStyle(work_1Style)

            work_2Style = TableStyle([
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTSIZE', (0,0), (-1,-1), 14),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Oblique'),
                ('TOPPADDING',(0,0),(-1,-1), 3),
                ('BOTTOMPADDING',(0,0),(-1,-1), 3),

            ])
            work_2.setStyle(work_2Style)

            tableStyle = TableStyle([
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTNAME', (0,0), (-1,-1), 'Verdana'),
                ('TOPPADDING',(0,0),(-1,-1), 5),
                ('BOTTOMPADDING',(0,0),(-1,-1), 12),

                ('FONTSIZE', (0,0), (-1,0), 16),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('BACKGROUND',(0,0),(-1,0), kolor_bg3),

                ('FONTSIZE', (0,1), (-1,-1), 12),
                ('TEXTCOLOR', (0,1), (-1,-1), colors.black),

            ])
            tablee.setStyle(tableStyle)


            for w in range (1, len(data)):
                if w % 2 == 0:
                    bc = kolor_bg2
                else:
                    bc = kolor_bg1

                tableBCStyle = TableStyle([
                    ('BACKGROUND',(0,w),(-1,w), bc),
                ])
                tablee.setStyle(tableBCStyle)

            table2Style = TableStyle([
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTNAME', (0,0), (-1,-1), 'Verdana'),
                ('TOPPADDING',(0,0),(-1,-1), 5),
                ('BOTTOMPADDING',(0,0),(-1,-1), 12),

                ('FONTSIZE', (0,0), (-1,0), 16),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('BACKGROUND',(0,0),(-1,0), kolor_bg3),

                ('FONTSIZE', (0,1), (-1,-1), 12),
                ('TEXTCOLOR', (0,1), (-1,-1), colors.black),

            ])
            table2.setStyle(table2Style)

            for w in range (1, len(data2)):
                if w % 2 == 0:
                    bc = kolor_bg2
                else:
                    bc = kolor_bg1

                table2BCStyle = TableStyle([
                    ('BACKGROUND',(0,w),(-1,w), bc),
                ])
                table2.setStyle(table2BCStyle)

            doc = SimpleDocTemplate(f"{nazwa_pliku[-2]}.pdf")

            doc.build(elements)

        except PermissionError:
            messagebox.showerror("Błąd", "Zamknij plik PDF")
        else:
            messagebox.showinfo("Info", "Pomyślnie zapisano do pliku pdf")
