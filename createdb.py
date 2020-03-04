import csv
import sqlite3
import tkinter
from tkinter import filedialog
rootsql=sqlite3.connect(database='varification.db')
cusors=rootsql.cursor()
cusors.execute('''CREATE TABLE MAINSCHE(ID INTEGER PRIMARY KEY AUTOINCREMENT)''')