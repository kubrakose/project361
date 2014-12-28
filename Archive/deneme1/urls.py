from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
#from urunler.views import new
from django.views.generic import ListView
from urunler.models import Post

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'deneme1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('urunler.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^urunler/', include('urunler.urls')),
    url(r'^blog/', ListView.as_view( queryset=Post.objects.all().order_by("-createddate"), template_name="blog.html")),
)
