__author__ = 'kubrakose'
# -*- coding: utf-8 -*-
import sys
from Tkinter import *
import ttk
import tkMessageBox
import Tkinter as tk
import tkFont
import ttk
from tkMessageBox import *
import sqlite3

vt=sqlite3.connect("products.db")
im=vt.cursor()
im.execute("""SELECT urunturu, marka, model, fiyat FROM vatan""")
veri1=im.fetchall()
im2=vt.cursor()
im2.execute("""SELECT urunturu2,marka2,model2,fiyat2 FROM bimeks""")
veri2=im2.fetchall()

class WantedResult(object):
    def __init__(self,veri):
        self.veri=veri
    def Comp(self,price):
        self.result=[]
        for tuples in self.veri:
            tuple=(tuples[-1].replace("tl","").split(",")[0])
            itemprice=int(tuple.replace(".",""))
            if price!="":
                if float(price)>itemprice:
                    self.result.append(tuples)
        return self.result
    def Withoutbrand(self,tur):
        self.res=[]
        for tup in self.veri:
            if tup[0]==tur:
                self.res.append(tup)
        return self.res

def producttypes(veri1,veri2):
    bos=[]
    for items1 in veri1:
        if items1[0] not in bos:
            bos.append(items1[0])
    for items2 in veri2:
        if items2[0] not in bos:
            bos.append(items2[0])
    return bos
types=producttypes(veri1,veri2)
def productvalues(liste):
    value=()
    for turler in liste:
        value+=(turler.encode(sys.stdout.encoding),)
    return value
ptv=productvalues(types)

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func
LARGE_FONT= ("Verdana", 12)


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Find Item")
        #tk.Tk.wm_geometry(self,"400x150")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = MainWindow(container, self)
        self.frames[MainWindow] = frame
        frame.grid(row=0, column=0, sticky=N+S+E+W)
        self.show_frame(MainWindow)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()




class MainWindow(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)

        dugme=tk.Button(self, text="Find", command=self.func)
        dugme.pack(side="left", padx=20, pady=40)
        dugme.grid(column=1, row=5, sticky="nsew")

        tus=tk.Button(self, text="Quit", command=quit)
        tus.place(relx=1.0, rely=0.5, anchor="s")
        tus.pack(side="right", padx=20, pady=40)
        tus.grid(column=4, row=5, sticky="nsew")

        producttypelabel=tk.Label(self, text="Choose product type")
        producttypelabel.grid(column=0, row=1, columnspan=2, sticky=N+S+E+W)
        self.producttype=ttk.Combobox(self, width="24")
        self.producttype['values']=ptv
        self.producttype.grid(column=3, row=1, columnspan=2, sticky=N+S+E+W)
        self.producttype.state(["readonly"])
        self.producttype.bind("<<ComboboxSelected>>")

        brandlabel=tk.Label(self, text="Enter a brand:")
        brandlabel.grid(column=0, row=2, columnspan=2, sticky=N+S+E+W)
        self.brand=StringVar()
        self.brand=tk.Entry(self, width="12", text=self.brand, justify="center")
        self.brand.grid(column=3, row=2, columnspan=2, sticky="nsew")

        pricelabel=tk.Label(self, text="Enter price limit:")
        pricelabel.grid(column=0, row=3, columnspan=2, sticky=N+S+E+W)
        self.price=StringVar()
        self.price=tk.Entry(self, width="12", text=self.price, justify="center")
        self.price.grid(column=3, row=3, sticky="nsew")
        self.price.bind('<KeyRelease>')

        #container = ttk.Frame()
        #container.pack(fill='both', expand=True)
        #self.tree = ttk.Treeview()
        #vertical = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        #horizantal = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        #self.tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizantal.set)
        #self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        #vertical.grid(column=1, row=0, sticky='ns', in_=container)
        #horizantal.grid(column=0, row=1, sticky='ew', in_=container)
        #container.grid_columnconfigure(0, weight=1)
        #container.grid_rowconfigure(0, weight=1)

    def func(self):
        urunturu=str(self.producttype.get())
        marka=str(self.brand.get().encode(sys.stdout.encoding).capitalize())
        fiyat=(int(self.price.get()))
        vt=sqlite3.connect("products.db")
        im=vt.cursor()
        if fiyat<0 or fiyat==0:
            tkMessageBox.showinfo("Invalid Price")
        elif fiyat=="":
            im.execute('SELECT * FROM vatan WHERE urunturu=? and marka=?', (urunturu,marka))
            veriv1=im.fetchall()

            print veriv1
            f=open("file.txt","w")
            for i in veriv1:
                f.write(str(i)+"\n")
            f.close()

            return veriv1,f
        if marka!="":
            im.execute('SELECT * FROM vatan WHERE urunturu=? and marka=?',(urunturu,marka))
            veri1=im.fetchall()
            compare=WantedResult(veri1)
            c=compare.Comp(fiyat)
            print c
            f=open("file.txt","w")
            for i in c:
                f.write(str(i) +"\n")
            f.close()

            #return compare.Comp(fiyat),f
        else:
            im.execute('SELECT * FROM vatan WHERE urunturu=?', (urunturu,))
            verii1=im.fetchall()
            sonuc=WantedResult(verii1)
            w=sonuc.Withoutbrand(urunturu)
            print w
            f=open("file.txt","w")
            for i in w:
                f.write(str(i)+"\n")
            f.close()
            #return sonuc.Withoutbrand(urunturu),f

        empty1=[]
        f=open("file.txt","r")
        for lines1 in f:
            empty1.append((lines1.replace("u'","").replace("(","").replace(")","").replace("'","").split(",")))
        print empty1

        #root=Tk()
        #root.columnconfigure(0, weight=1)
        #root.rowconfigure(0, weight=1)
        #root.title("Find Item")

        #tree=ttk.Treeview(tk.Toplevel())

       #verticall = ttk.Scrollbar(orient="vertical", command=tree.yview)
       #horizantall = ttk.Scrollbar(orient="horizontal", command=tree.xview)

       ##tree.configure(yscrollcommand=verticall.set, xscrollcommand=horizantall.set)
       ##tree.grid(column=0, row=0, sticky='nsew', in_=productsframe)
       ##verticall.grid(column=1, row=0, sticky='ns')
       ##horizantall.grid(column=0, row=1, sticky='ew')
       ##productsframe.grid_columnconfigure(0, weight=1)
       ##productsframe.grid_rowconfigure(0, weight=1)

       #tree.pack()

        n=tk.Toplevel(self)

        s=ttk.Scrollbar(n)
        s.pack(side="right", fill="y" )

        self.tree = ttk.Treeview(n, yscrollcommand=s.set)
        self.tree.pack()



        self.tree["columns"]=("one","two","three","four")
        self.tree.column("one")
        self.tree.column("two")
        self.tree.heading("one", text="tur")
        self.tree.heading("two", text="model")
        self.tree.column("three")
        self.tree.column("four")
        self.tree.heading("three", text="marka")
        self.tree.heading("four", text="fiyat")

        for item in empty1:
            self.tree.insert("" , "end", values=item)


app = Application()
app.mainloop()
