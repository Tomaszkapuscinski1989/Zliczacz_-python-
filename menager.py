from contextlib import contextmanager
import sqlite3 as sq
from tkinter import *
from tkinter import ttk

font_m = ("Times", "14")
font_d = ("Times", "18")
kolor_bg1 = "#f7f8f9"
kolor_bg2 = "#ccd3de"
kolor_bg3 = "#3a4454"
kolor_text1 = "black"
kolor_text2 = "white"


@contextmanager
def open_base(name):
    try:
        conn = sq.connect(name)
        c = conn.cursor()
        yield c
    finally:
        conn.commit()
        conn.close()

