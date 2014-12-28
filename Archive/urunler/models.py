from django.db import models
import sqlite3
from django.core.files import File
# Create your models here.

class WantedResult(models.Model):
    def Showresult(self,veri,prices):
        self.result=[]
        price=prices.split("-")
        for tuples in veri:
            tuple=(tuples[-1].replace("tl","").split(",")[0])
            itemprice=int(tuple.replace(".",""))
            if float(price[1])>itemprice>float(price[0]):
                self.result.append(tuples)
        return self.result

def producttypes():
    empty=[]
    conn=sqlite3.connect("productsdata.db")
    bimeks=conn.cursor()
    bimeks.execute("""SELECT urunturu2, marka2, model2, urls2, fiyat2 FROM bimeks""")
    verib=bimeks.fetchall()
    vatan=conn.cursor()
    vatan.execute("""SELECT urunturu, marka, model, url, fiyat FROM vatan""")
    veriv=vatan.fetchall()
    for items1 in veriv:
        if items1[0] not in empty:
            empty.append(items1[0])
    for items2 in verib:
        if items2[0] not in empty:
            empty.append(items2[0])
    return empty

def allbrands():
    empty=[]
    conn=sqlite3.connect("productsdatabase.db")
    #bimeks=conn.cursor()
    #bimeks.execute("""SELECT urunturu2, marka2, model2, fiyat2 FROM bimeks""")
    #verib=bimeks.fetchall()
    vatan=conn.cursor()
    vatan.execute("""SELECT urunturu, marka, model,url, fiyat FROM vatan""")
    veriv=vatan.fetchall()
    for items1 in veriv:
        if items1[1] not in empty:
            empty.append(items1[1])
    #for items2 in verib:
    #    if items2[1] not in empty:
    #        empty.append(items2[1])
    return empty

def tablo(x):
    dosya=open(x,"r")
    m=File(dosya)
    b=[]
    y=[]
    liste=[]
    for line in m:
        print (line.replace("'","\"").split("u\""))
        b.append((line.replace("'","\"").split("u\"")))
        print type((line.replace("'","\"").split("u\"")))
        print len((line.replace("'","\"").split("u\"")))
    for i in b:
        print i
        for ii in i:
            if ii.replace("(","").replace('",',"").replace("\")\n","")!="":
                y.append(ii.replace("(","").replace('",',"").replace("\")\n",""))
    #for r in y: print(r)
    for i in range(len(y)):
        if y[0:5]!=[]:
            liste.append(y[0:5])
            del y[0:5]
    print liste
    return liste

def howmany(x):
    print(len(x))
    return len(x)

class Post(models.Model):
    title=models.CharField(max_length=100)
    body=models.TextField()
    createddate=models.DateTimeField()

    def __unicode__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=50)

    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)


