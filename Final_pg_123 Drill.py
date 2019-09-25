from tkinter import *
from tkinter import Tk
from tkinter import filedialog
import shutil
import os
import sqlite3
import time

#============================== GUI Layout ============================================
class ParentWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self)

        self.master = master
        self.master.resizable(width= False, height= False)
        self.master.geometry('{}x{}'.format(600, 300))
        self.master.title('Move Text Files')
        self.master.config(bg='lightgray')

        self.varInputFrom = StringVar()
        self.varInputTo = StringVar()
# ========================================Move From GUI=================================================

        self.lblFrom = Label(self.master, text='Move From: ', font=("Helvetica", 16), fg='black', bg='lightgray')
        self.lblFrom.grid(row=0, column=0, padx=(30, 0), pady=(30, 0))

        self.txtInputFrom = Entry(self.master, text=self.varInputFrom, font=("Helvetica", 12), fg='black', bg='white')
        self.txtInputFrom.grid(row=0, column=1, padx=(0, 0), pady=(30, 0), columnspan=6)

        self.btnCheckFrom = Button(self.master, text="Browse From ", width=13, height=2, command=self.BrowseFrom)
        self.btnCheckFrom.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky=S + W)

#========================================Move To GUI=================================================

        self.txtInputTo = Entry(self.master, text=self.varInputTo, font=("Helvetica", 12), fg='black', bg='white')
        self.txtInputTo.grid(row =2, column=1, padx=(0, 0), pady=(0, 0), columnspan=6)

        self.lblTo = Label(self.master, text='Move To: ', font=("Helvetica", 16), fg='black', bg='lightgray')
        self.lblTo.grid(row=2, column=0, padx=(50, 0), pady=(0, 0))

        self.btnCheckTo = Button(self.master, text="Browse To ", width=13, height=2, command=self.BrowseTo)
        self.btnCheckTo.grid(row=3, column=0, padx=(20, 0), pady=(10, 0), sticky=S + W)

#=======================================Buttons GUI==================================================

        self.btnMove = Button(self.master, text="Move Files", width=14, height=2, command=self.MoveFiles)
        self.btnMove.grid(row=3, column=3, padx=(0, 30), pady=(10, 0), sticky=E)

        self.btnclose = Button(self.master, text="Cancel", width=14, height=2, command = self.close)
        self.btnclose.grid(row=3, column=6, padx=(0,0), pady=(10,0), sticky=E)

    def close(self):
        self.master.destroy()

    def BrowseTo(self):
        dst = filedialog.askdirectory()
        self.varInputTo.set(dst)
        return dst
        print(dst)

    def BrowseFrom(self):
        src = filedialog.askdirectory()
        self.varInputFrom.set(src)
        return src
        print(src)

#======================================== Database Creation =============================================================

    def Database_create():
        conn = sqlite3.connect('MovedFile_DB.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS files (ID INTEGER PRIMARY KEY AUTOINCREMENT,file_name TEXT, mod_date DATE)")
            conn.commit()
        conn.close()
        
    Database_create()
        
# ======================================== File Manipulation =============================================================
    def MoveFiles(self):
        conn = sqlite3.connect('MovedFile_DB.db')
        with conn:
            cursor = conn.cursor()
            dst=self.varInputTo.get()
            src=self.varInputFrom.get()
            for file in os.listdir(src):
                if file.endswith(".txt"):
                    prop = os.path.getmtime(src)
                    join = os.path.join(src, file)
                    shutil.move(join, dst)
                    date = time.ctime(prop)
                    insert = 'INSERT INTO files (file_name, mod_date) VALUES (?,?)'
                    cursor.execute(insert, [file,date])
                    conn.commit()
                    print(join, date)
        conn.close()

if __name__ == "__main__":
    root = Tk()
    app = ParentWindow(root)
    root.mainloop()
