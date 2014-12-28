__author__ = 'kubrakose'
# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
import unicodedata
import sys
import sqlite3
def convertletter(str):
    letters = [('İ','I'), ('Ğ','G'),('Ü','U'), ('Ş','S'), ('Ö','O'),('Ç','C'),('ı','i'),
                ('ğ','g'),('ş','s'),('ö','o'),('ç','c'),('ü','u'),('(',''),(')',''),('[',''),(']','')]
    for wanted , letter in letters:
        str  = str.replace(wanted , letter)
    return str
def tursayfa(x):
    ht=[]
    k=[]
    html=urllib2.urlopen(x)
    soup=BeautifulSoup(html)
    for s in soup.findAll("a"):
        ht.append(s.get("href"))
    for h in ht[14:128]:
        s=unicodedata.normalize("NFKD",h).encode('ascii','ignore')
        if s[0]=="/":
            url="http://www.vatanbilgisayar.com"+s
            if ([s.strip("/"),url]) not in k:  ###aynı sayfadan birden fazla olmamasi icin yoksa asagida index hatasi veriyo
                k.append([s.strip("/"),url])
    return k
    #for e in k: print e     #[urun turleri,internet sayfası]
turs=tursayfa("http://www.vatanbilgisayar.com/")
#print(turs)
def tumsayfalar(k):
    for kk in range((len(k))):
        v=urllib2.urlopen(k[kk][1])
        sou=BeautifulSoup(v)
        linkler=sou.findAll("a",{"id":"ctl00_u20_ascUrunList_ascPagingDataUst_lnkNext"})
        if linkler==[]:
            azsayfa=[]
            for pp in sou.findAll("a"):
                if pp.get("href") not in azsayfa:
                    azsayfa.append(pp.get("href"))
            for p in azsayfa:
                if "page" in p:
                    y="http://www.vatanbilgisayar.com"+p
                    k[kk].append(y)
            #print(k[kk])
        if linkler!=[]:
            i=1
            while i<len(k[kk]):
                ht=urllib2.urlopen(k[kk][-1])
                so=BeautifulSoup(ht)
                li=so.findAll("a",{"id":"ctl00_u20_ascUrunList_ascPagingDataUst_lnkNext"})   #urunlerin tum sayfalarini almak için ileri butonunun tagi
                for t1 in li:
                    m=("http://www.vatanbilgisayar.com"+t1.get("href"))
                    (k[kk]).append(unicodedata.normalize("NFKD",m).encode('ascii','ignore'))  #yukaridaki listayi [[urunturu,urunilksayfasi,urunikinci sayfasi],...] sekline getiriyo
                i=i+1
            ys=[]
            hh=urllib2.urlopen(k[kk][-1])
            sso=BeautifulSoup(hh)
            for syf in sso.findAll("a"):
                if syf.get("href") not in ys:
                    ys.append(syf.get("href"))
                for ssyf in ys:
                    if "page" in ssyf:
                        ye="http://www.vatanbilgisayar.com"+ssyf
                        if ye not in k[kk]:
                            k[kk].append(ye)
    return  k
            #print bos[o]
#for w in k: print w
    #print k[kk][1]
#for w in k:print w
tums=tumsayfalar(turs)
#print(tums)
#for i in tums:print(i)

def isimfiyat(k):
    isimler=[]
    fiyatlar=[]
    markalar=[]
    urls=[]
    for p in range(len(k)):
        if k[p][0] not in isimler:
            isimler.append([k[p][0]])
        if k[p][0] not in fiyatlar:
            fiyatlar.append([k[p][0]])
        if k[p][0] not in markalar:
            markalar.append([k[p][0]])
        if k[p][0] not in urls:
            urls.append([k[p][0]])
        print(isimler)
        print(urls)
        i=1
        while i<len(k[p]):
            bos=[]
            uu=urllib2.urlopen(k[p][i])
            ss=BeautifulSoup(uu)
            for f in ss.findAll("span",{"class":"prdBrd"}):
                markalar[next((i0 for i0, sublist0 in enumerate(markalar) if k[p][0] in sublist0))].append(f.getText())
            for f in ss.findAll("span",{"class":"prdName"}): #sayfadan urun isimini aliyo
                if f.find("a")!=None:
                    if f.find("a") not in bos:
                        bos.append(f.find("a"))
                isimler[next((i for i, sublist in enumerate(isimler) if k[p][0] in sublist))].append(unicodedata.normalize("NFKD",f.getText()).encode('ascii','ignore')) #eger urunturu(orn: ceptel) daha önce girilmisse modelleri onun listesine ekliyo (isimler=nested list)
            for ff in ss.findAll("div",{"class":"urunListe_satisFiyat"}): #sayfadan urun fiyatını aliyo
                fiyatlar[next((ii for ii, sublisti in enumerate(fiyatlar) if k[p][0] in sublisti))].append(ff.getText()) #eger urunturu(orn: ceptel) daha önce girilmisse modellerin fiyatlarini onun listesine ekliyo (fiyatlar=nested list)
            for fff in bos:
                if fff.get("href")[0]=="/" and (fff.get("href")).split(".")[-1]=="html":
                    u="http://www.vatanbilgisayar.com"+fff.get("href")
                    print(u)
                    urls[next((iu for iu, sublistiu in enumerate(urls) if k[p][0] in sublistiu))].append(u) #eger urunturu(orn: ceptel) daha önce girilmisse modellerin fiyatlarini onun listesine ekliyo (fiyatlar=nested list)
                    print(urls)
            i=i+1
    ###sadece turunturu yazan liste icineki listeleri silmak icin cunku bazi urunlerin model veya fiyati yok yazlnızca urunturu yaziyo asagida index hatası veriyo
    print urls
    sil=0
    sill=0
    ssil=0
    silu=0
    while ssil<len(markalar):
        if len(markalar[ssil])==1:
            del(markalar[ssil])
        ssil=ssil+1
    while sil<(len(isimler)):
        if len(isimler[sil])==1:
            del(isimler[sil])
        sil=sil+1
    while sill<(len(fiyatlar)):
        if len(fiyatlar[sill])==1:
            del(fiyatlar[sill])
        sill=sill+1
    while silu<len(urls):
        if len(urls[silu])==1:
            del(urls[silu])
        silu=silu+1
    #for m in markalar: print m
    #for y in isimler: print y
    #for yy in fiyatlar: print yy
    #for u in urls: print u
    ####isimler ile fiyatlar in uzunluklarinin aynı olması lazım!!!!
    print len(markalar)
    print len(isimler)
    print len(fiyatlar)
    print(len(urls))
    tum=[]
    for item in range(len(isimler)):
        for items in range(len(fiyatlar)):
            for itm in range(len(markalar)):
                for itemsu in range(len(urls)):
                    if isimler[item][0]==fiyatlar[items][0]==markalar[itm][0]==urls[itemsu][0]:
                        a=1
                        b=1
                        c=1
                        d=1
                        while a<len(isimler[item]):
                            tum.append((isimler[item][0].replace("-"," ").capitalize(),markalar[itm][c].capitalize(),isimler[item][a].replace("-"," ").capitalize(),urls[itemsu][d],fiyatlar[items][b].capitalize()))
                            a=a+1
                            b=b+1
                            c=c+1
                            d=d+1
    print tum
    return tum
turmodelfiyat=isimfiyat(tums)
for i in turmodelfiyat:
    for ii in i:
        print ii

#db=sqlite3.connect("products.db")
#db=sqlite3.connect("productsdata.db")
#im=db.cursor()
#im.execute("""CREATE TABLE vatan(urunturu, marka, model, url, fiyat)""")
#im.executemany("""INSERT INTO vatan VALUES (?,?,?,?,?)""", turmodelfiyat)
#db.commit()
#
#data=im.fetchall()
#print data
