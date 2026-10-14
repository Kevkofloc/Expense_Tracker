import sqlite3 as sql
import customtkinter as tk
from Functions import neu_Ausgabe, KategorieWahl,datum
from Grafiken import *
import datetime
conn = sql.connect('Investments.db')
cursor = conn.cursor()
datum()
#Create Tables
cursor.execute('''CREATE TABLE IF NOT EXISTS Investments(
    id INTERGER PRIMARY KEY,
    menge INTEGER NOT NULL,
    kategorie TEXT NOT NULL,
    datum TEXT NOT NULL,
    monat TEXT NOT NULL,
    jahr INTEGER NOT NULL)
    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Einteilungen(
    k_ID INTERGER PRIMARY KEY,
    kategorie TEXT NOT NULL,
    ausgaben INTEGER NOT NULL)
    ''')

conn.close()

#define root
root = tk.CTk()
root.title('Investments')
root.geometry('500x500')

#add objects
tk.CTkLabel(root, text='Investments' , font=("Arial", 26, "bold")).pack()
tk.CTkLabel(root, text='Geben SIe ihre Ausgaben an').pack()
add = tk.CTkButton(root, text='Add',fg_color="#8b0000",width=200, height=50, command=lambda x = root:neu_Ausgabe(x))
show = tk.CTkButton(root, text='Show Kategory',width=200, height=50, command= lambda x = root: KategorieWahl(root))
graph = tk.CTkButton(root, text="show graph", fg_color="darkgreen",width=200, height=50,command= lambda x = root: choose(root))
add.pack()
show.pack()
graph.pack()

root.mainloop()


