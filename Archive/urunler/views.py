from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from models import producttypes
from models import allbrands
# Create your views here.
import unicodedata
from django.shortcuts import render_to_response
import sqlite3
from models import WantedResult
from models import tablo,howmany
from models import Category
from models import Post
import models
from django.views.generic import View
from django.template import Template,Context
from django.core.files import File

def home(request):
    return render_to_response("ht1.html")


@csrf_exempt
def mysearch(request):

    if request.method == "GET":
        pliste=producttypes()
        return render_to_response("base.html",{"products":pliste})

    elif request.method == "POST":

        searchterm = request.POST.get("tur")
        searchbrand = (request.POST.get("brand")).capitalize()
        searchp = request.POST.get("price")
        print(searchterm)
        print(searchbrand)
        conn=sqlite3.connect("productsdata.db")
        vatan=conn.cursor()
        bimeks=conn.cursor()
        print searchterm
        if searchterm=="All" and searchbrand=="":
            vatan.execute('SELECT * FROM vatan' )
            bimeks.execute('SELECT * FROM bimeks')
            veriva=vatan.fetchall()
            veribi=bimeks.fetchall()
            compare=WantedResult()
            resultv=(compare.Showresult(veriva,searchp))
            resultb=(compare.Showresult(veribi,searchp))
            print resultv
            print resultb
            results=resultv+resultb
            resultslengt=howmany(results)
            return render_to_response("yeni.html",{"rakam":resultslengt,"sonuclar":results})
        elif searchterm=="All" and searchbrand!="":
            vatan.execute('SELECT * FROM vatan WHERE marka=?',(searchbrand,))
            bimeks.execute('SELECT * FROM bimeks WHERE marka2=?', (searchbrand,))
            veriva=vatan.fetchall()
            veribi=bimeks.fetchall()
            compare=WantedResult()
            resultv=(compare.Showresult(veriva,searchp))
            resultb=(compare.Showresult(veribi,searchp))
            print resultv
            print resultb
            results=resultv+resultb
            resultslengt=howmany(results)
            return render_to_response("yeni.html",{"rakam":resultslengt,"sonuclar":results})
        else:
            vatan.execute('SELECT * FROM vatan WHERE urunturu=? and marka=?',(searchterm,searchbrand))
            bimeks.execute('SELECT * FROM bimeks WHERE urunturu2=? and marka2=?', (searchterm,searchbrand))
            veriv=vatan.fetchall()
            verib=bimeks.fetchall()
            print verib
            #(veri)
            #for i in veri:
                #for ii in i:
                    #print ii,
            compare=WantedResult()
            resultv=(compare.Showresult(veriv,searchp))
            resultb=(compare.Showresult(verib,searchp))
            print resultv
            print resultb
            results=resultv+resultb
            #f=open("file.txt","w")
            #mf=File(f)
            #for i in results:
            #    mf.write(str(i) +"\n")
            #pliste=producttypes()
            #bliste=allbrands()
            #l=tablo("file.txt")
            resultslengt=howmany(results)
            return render_to_response("yeni.html",{"rakam":resultslengt,"sonuclar":results})

#@csrf_exempt
#def new(request):
##    l=tablo("file.txt")
##    r=howmany(l)
#    categories = Category.objects.filter()
#    a=Post()
#    return render_to_response("blog.html",{"post":a})



categories = Category.objects.filter()