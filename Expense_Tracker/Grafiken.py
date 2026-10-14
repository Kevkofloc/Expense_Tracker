import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import customtkinter as tk
import sqlite3 as sql

from pandas.core.base import SelectionMixin

from Functions import *
conn = sql.connect('Investments.db')
cursor = conn.cursor()
def choose(root):
    root1 = tk.CTkToplevel(root)
    tk.CTkLabel(root1,text="Timespan?").pack()
    optionen = ["1 month","3 months","1 Year", "3 Years", "10 Years", "Since beginning"]
    zeitspanne = tk.CTkComboBox(root1,values=optionen)
    zeitspanne.pack()
    tk.CTkLabel(root1,text="Kategory?").pack()
    cursor.execute("SELECT kategorie FROM Einteilungen")
    kategorie = cursor.fetchall()
    Kat = ["Alle"]
    for i in kategorie:
        Kat.append(i[0])
    auswahlKategorie = tk.CTkComboBox(root1,values=Kat)
    auswahlKategorie.pack()
    enter = tk.CTkButton(root1,text="Enter",command=lambda: show(zeitspanne.get(),auswahlKategorie.get(),root,root1))
    enter.pack()
def show(zeitspanne, Kategorie, root,root1):
    root1.destroy()
    date,monat,jahr = datum()
    if Kategorie == "Alle":
        if zeitspanne == "1 month":
            cursor.execute("SELECT datum,menge FROM Investments WHERE jahr = jahr AND monat = monat")
        elif zeitspanne == "3 months":
            cursor.execute("SELECT monat,menge FROM Investments WHERE jahr = jahr ORDER BY monat DESC LIMIT monat-3")
        elif zeitspanne == "1 Year":
            cursor.execute("SELECT monat,menge FROM Investments WHERE jahr = jahr ORDER BY monat DESC ")
        elif zeitspanne == "3 Years":
            cursor.execute("SELECT jahr,menge FROM Investments ORDER BY jahr DESC LIMIT jahr-3")
        elif zeitspanne == "10 Years":
            cursor.execute("SELECT jahr,menge FROM Investments ORDER BY jahr DESC LIMITj jahr- 10")
        elif zeitspanne == "Since beginning":
            cursor.execute("SELECT jahr,menge FROM Investments ORDER BY jahr DESC")

    else:
        if zeitspanne == "1 month" :
            cursor.execute("SELECT datum,menge FROM Investments WHERE jahr = jahr AND monat = monat AND kategorie = ?", (Kategorie,))
        elif zeitspanne == "3 months":
            cursor.execute("SELECT monat,menge FROM Investments WHERE jahr = jahr AND kategorie = ? ORDER BY monat DESC LIMIT monat-3",(Kategorie,))
        elif zeitspanne == "1 Year":
            cursor.execute("SELECT monat,menge FROM Investments WHERE jahr = jahr ORDER BY monat DESC ")
        elif zeitspanne == "3 Years":
            cursor.execute("SELECT jahr,menge FROM Investments ORDER BY jahr DESC LIMIT 3")
        elif zeitspanne == "10 Years":
            cursor.execute("SELECT jahr,menge FROM Investments ORDER BY jahr DESC LIMIT 10")
        elif zeitspanne == "Since beginning":
            cursor.execute("SELECT jahr,menge FROM Investments ORDER BY jahr DESC")
    Liste = cursor.fetchall()
    d = Liste[0][0]
    x = []
    y = []
    z = 0
    for i in Liste:
        if d != i[0]:
            x.append(d)
            y.append(z)
            z = 0
            d = i[0]
        z += i[1]

    x.append(d)
    y.append(z)

    plt.plot(x,y)
    plt.xlabel("Datum")
    plt.ylabel("Ausgaben")
    plt.show()





