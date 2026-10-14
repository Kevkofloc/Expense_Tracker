import customtkinter as tk
import sqlite3 as sql
import datetime
import requests

def datum():
    heute = datetime.date.today()
    return heute.day, heute.month, heute.year

conn = sql.connect('Investments.db')
cursor = conn.cursor()
def neu_Ausgabe(root):
    root1 = tk.CTkToplevel(root)
    root1.geometry('300x300')
    root1.title('Ausgabe')
    tk.CTkLabel(root1, text='Wie viel Geld?').pack()
    G = tk.CTkEntry(root1)
    G.pack()
    tk.CTkLabel(root1, text='Kategorie?').pack()
    K = tk.CTkEntry(root1)
    K.pack()
    tk.CTkButton(root1, text="Add", command=lambda: eintragen(G.get(), K.get(), root1)).pack()
    root1.mainloop()

def eintragen(G,K,root1):
    if K == "" :
        return
    if G == "" :
        G = 0
    if G.isnumeric() == False:
        print("Error")
        return
    cursor.execute("SELECT Kategorie FROM Einteilungen")
    kategorie = False
    for i in cursor.fetchall():
        if K in i:
            kategorie = True
    if not kategorie:
        cursor.execute("SELECT K_ID FROM Einteilungen")
        K_id = 0
        for i in cursor.fetchall():
            K_id = i[0]
        K_id += 1
        cursor.execute('''INSERT INTO Einteilungen (K_ID,Kategorie,Ausgaben) VALUES (?,?,?) ''', (K_id, K, 0))
    cursor.execute("SELECT id FROM Investments")
    id = 0
    for i in cursor.fetchall():
        id = i[0]
    id += 1
    date,monat,jahr = datum()
    cursor.execute('''INSERT INTO Investments (id,Menge,Kategorie,datum, monat, jahr) VALUES (?,?,?,?,?,?)''', (id, G, K,date,monat,jahr))
    conn.commit()
    cursor.execute("SELECT Ausgaben FROM Einteilungen WHERE Kategorie = ?", (K,))
    investments = cursor.fetchall()
    cursor.execute("UPDATE Einteilungen SET Ausgaben = ?  WHERE Kategorie = ?", (investments[0][0]+int(G), K))
    conn.commit()
    print("Done")
    root1.destroy()

def KategorieWahl(root):
    root1 = tk.CTkToplevel(root)
    tk.CTkLabel(root1, text='Kategorie').pack()
    Kat = tk.CTkEntry(root1)
    Kat.pack()
    chosen = tk.CTkButton(root1, text='Choose', command=lambda: showKategorie(root,root1, Kat.get()))
    chosen.pack()
    cursor.execute("SELECT Kategorie FROM Einteilungen")
    kategorien = cursor.fetchall()
    tk.CTkLabel(root1, text='Kategorien:').pack()
    for i in kategorien:
        k = tk.CTkLabel(root1, text=i[0], font=('Arial', 10))
        k.pack()
    root1.mainloop()

def showKategorie(root,root1,Kategorie):
    cursor.execute("SELECT menge, datum,monat,jahr FROM  Investments WHERE kategorie = ?", (Kategorie,))
    ausgaben = cursor.fetchall()
    root1.destroy()
    root2 = tk.CTkToplevel(root)
    root2.geometry('400x400')

    summe = 0
    tk.CTkLabel(root2,text=Kategorie,font=("Arial", 20, "bold")).pack()
    for i in ausgaben:
        tk.CTkLabel(root2, text= f"{i[1]}.{i[2]}.{i[3]}: {i[0]}€").pack()
    cursor.execute("SELECT Ausgaben FROM Einteilungen WHERE Kategorie = ?", (Kategorie,))
    summe = cursor.fetchall()
    tk.CTkLabel(root2, text=f"Insgesamt: {summe[0][0]}€", bg_color="darkred").pack()

    root2.mainloop()







