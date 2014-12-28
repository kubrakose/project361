__author__ = 'kubrakose'
# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
import unicodedata
import sqlite3

def tursayfa(x):
    ht=[]
    k=[]
    html=urllib2.urlopen(x)
    soup=BeautifulSoup(html)
    for s in soup.findAll("a"):
        ht.append(s.get("href"))
    for h in ht:
        s=unicodedata.normalize("NFKD",h).encode('ascii','ignore')
        if s[0]=="/":
            url="http://www.bimeks.com.tr"+s
            if ([s.strip("/"),url]) not in k:  ###aynı sayfadan birden fazla olmamasi icin yoksa asagida index hatasi veriyo
                if "kategori/" in s.strip("/"):
                    k.append([s.strip("/")[14:],url])
    return k
    #for e in k: print e     #[urun turleri,internet sayfası]
turs=tursayfa("http://www.bimeks.com.tr/")
print turs
def allpages(k):
    for kk in range(len(k)):
        i=0
        while i<len(k[kk]):
            v=urllib2.urlopen(k[kk][-1])
            soup=BeautifulSoup(v)
            for pp in soup.findAll("a"):
                azsayfa=[]
                if pp.get("href") not in azsayfa:
                    azsayfa.append(pp.get("href"))
                for p in azsayfa:
                    if type(p)==unicode:
                        s=unicodedata.normalize("NFKD",p).encode('ascii','ignore')
                        if "/kategori.aspx?kid=" and "sn=" in s:
                            y="http://www.bimeks.com.tr"+s
                            if y not in k[kk]:
                                k[kk].append(y)
            i=i+1
    return k
tums=allpages(turs)
for i in tums: print i
def isimfiyat(k):
    isimler=[]
    fiyatlar=[]
    markalar=[]
    urls=[]
    for p in range(len(k)):
        if k[p][0] not in isimler:
            markalar.append([k[p][0]])
        if k[p][0] not in isimler:
            isimler.append([k[p][0]])
        if k[p][0] not in isimler:
            fiyatlar.append([k[p][0]])
        if k[p][0] not in urls:
            urls.append([k[p][0]])
        i=1
        while i<len(k[p]):
            a=[]
            uu=urllib2.urlopen(k[p][i])
            ss=BeautifulSoup(uu)
            for m in ss.findAll("div",{"class":"thumbnail"}):
                for brand in m.findAll("a"):
                    if brand!=None:
                        markalar[next((im for im, sublistm in enumerate(markalar) if k[p][0] in sublistm))].append(brand.get("title").split("-")[0])
            for f in ss.findAll("div",{"class":"thumbnail"}): #sayfadan urun isimini aliyo
                for title in f.findAll("a"):
                    if title.get("title")!=None:
                        isimler[next((i for i, sublist in enumerate(isimler) if k[p][0] in sublist))].append(title.get("title")) #eger urunturu(orn: ceptel) daha önce girilmisse modelleri onun listesine ekliyo (isimler=nested list)
            for ff in ss.findAll("span",{"class":"vatBig"}): #sayfadan urun fiyatını aliyo
                if ff!=None:
                    fiyatlar[next((ii for ii, sublisti in enumerate(fiyatlar) if k[p][0] in sublisti))].append(ff.getText()) #eger urunturu(orn: ceptel) daha önce girilmisse modellerin fiyatlarini onun listesine ekliyo (fiyatlar=nested list)
            for yy in ss.findAll("div",{"class":"info"}):
                if yy.find("h2")!=None:
                    if (yy.find("a")) not in a:
                        if (yy.find("a")) != None:
                            a.append((yy.find("a")))
            for ui in a:
                if "/urun/" in (ui.get("href")).encode("utf-8"):
                    url="http://www.bimeks.com.tr/"+ui.get("href")
                    if url not in urls:
                        urls[next((iui for iui, sublistiu in enumerate(urls) if k[p][0] in sublistiu))].append(url) #eger urunturu(orn: ceptel) daha önce girilmisse modellerin fiyatlarini onun listesine ekliyo (fiyatlar=nested list)
                        #urls.append(url)
            i=i+1
    print urls
        ###sadece turunturu yazan liste icineki listeleri silmak icin cunku bazi urunlerin model veya fiyati yok yazlnızca urunturu yaziyo asagida index hatası veriyo
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
    while silu<(len(urls)):
        if len(urls[silu])==1:
            del(urls[silu])
        silu=silu+1
        ####isimler ile fiyatlar in uzunluklarinin aynı olması lazım!!!!
    tum=[]
    for item in range(len(isimler)):
        for items in range(len(fiyatlar)):
            for itm in range(len(markalar)):
                for itemu in range(len(urls)):
                    if isimler[item][0]==fiyatlar[items][0]==markalar[itm][0]==urls[itemu][0]:
                        a=1
                        while a<len(isimler[item]):
                            tum.append((isimler[item][0].replace("-"," ").replace(".aspx","").capitalize(),markalar[itm][a].capitalize(),isimler[item][a].replace("-"," ").capitalize(),urls[itemu][a],fiyatlar[items][a].capitalize()))
                            a=a+1
    return tum
turmarkamodelfiyat=isimfiyat(tums)
for i in turmarkamodelfiyat:
    for ii in i:
        print ii

db=sqlite3.connect("productsdata.db")
im=db.cursor()
im.execute("""CREATE TABLE bimeks(urunturu2, marka2, model2, urls2, fiyat2)""")
im.executemany("""INSERT INTO bimeks VALUES (?,?,?,?,?)""", turmarkamodelfiyat)
db.commit()

