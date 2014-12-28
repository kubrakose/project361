__author__ = 'kubrakose'
from django.conf.urls import patterns, include, url
from django.views.generic import ListView, TemplateView, DetailView
from .views import mysearch
from .models import Post
#from .views import new
#from urunler.views import Dnm

urlpatterns = patterns('',
    url(r'^$',mysearch),
    #url(r'^result', new),
    url(r'^$', ListView.as_view(queryset=mysearch, template_name="base.html")),
    #url(r'^results', new),
    #url(r'^blog/', ListView.as_view(queryset=Post.objects.all().order_by("-createddate"), template_name="blog.html")),
)
