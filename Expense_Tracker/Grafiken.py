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
    date,month,year = datum()
    # Hilfsberechnungen für Zeitspannen (Beispiel basierend auf aktuellen year und month Variablen)
# Für 3 Monate: Berechne Startjahr und Startmonat
    target_month = month - 3
    target_year = year
    if target_month <= 0:
        target_month += 12
        target_year -= 1
    
    # Für Jahre
    year_3_years = year - 3
    year_10_years = year - 10
    
    if Kategorie == "Alle":
        if zeitspanne == "1 month":
            cursor.execute("SELECT datum, menge FROM Investments WHERE jahr = ? AND monat = ?", (year, month))
        elif zeitspanne == "3 months":
            # Entweder über kombiniertes Jahr/Monat oder Filter über >=
            cursor.execute(
                """SELECT jahr, monat, menge FROM Investments 
                   WHERE (jahr > ? OR (jahr = ? AND monat >= ?)) AND (jahr < ? OR (jahr = ? AND monat <= ?))
                   ORDER BY jahr DESC, monat DESC""",
                (target_year, target_year, target_month, year, year, month)
            )
        elif zeitspanne == "1 Year":
            cursor.execute("SELECT monat, menge FROM Investments WHERE jahr = ? ORDER BY monat DESC", (year,))
        elif zeitspanne == "3 Years":
            cursor.execute("SELECT jahr, monat, menge FROM Investments WHERE jahr >= ? ORDER BY jahr DESC, monat DESC", (year_3_years,))
        elif zeitspanne == "10 Years":
            cursor.execute("SELECT jahr, monat, menge FROM Investments WHERE jahr >= ? ORDER BY jahr DESC, monat DESC", (year_10_years,))
        elif zeitspanne == "Since beginning":
            cursor.execute("SELECT jahr, monat, menge FROM Investments ORDER BY jahr DESC, monat DESC")
    
    else:
        if zeitspanne == "1 month":
            cursor.execute("SELECT datum, menge FROM Investments WHERE jahr = ? AND monat = ? AND Kategorie = ?", (year, month, Kategorie))
        elif zeitspanne == "3 months":
            cursor.execute(
                """SELECT jahr, monat, menge FROM Investments 
                   WHERE Kategorie = ? AND ((jahr > ? OR (jahr = ? AND monat >= ?)) AND (jahr < ? OR (jahr = ? AND monat <= ?)))
                   ORDER BY jahr DESC, monat DESC""",
                (Kategorie, target_year, target_year, target_month, year, year, month)
            )
        elif zeitspanne == "1 Year":
            cursor.execute("SELECT monat, menge FROM Investments WHERE jahr = ? AND Kategorie = ? ORDER BY monat DESC", (year, Kategorie))
        elif zeitspanne == "3 Years":
            cursor.execute("SELECT jahr, monat, menge FROM Investments WHERE Kategorie = ? AND jahr >= ? ORDER BY jahr DESC, monat DESC", (Kategorie, year_3_years))
        elif zeitspanne == "10 Years":
            cursor.execute("SELECT jahr, monat, menge FROM Investments WHERE Kategorie = ? AND jahr >= ? ORDER BY jahr DESC, monat DESC", (Kategorie, year_10_years))
        elif zeitspanne == "Since beginning":
            cursor.execute("SELECT jahr, monat, menge FROM Investments WHERE Kategorie = ? ORDER BY jahr DESC, monat DESC", (Kategorie,))

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





