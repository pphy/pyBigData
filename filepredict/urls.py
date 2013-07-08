from django.conf.urls import patterns, include, url
from django.conf import settings
from predictfilm.views import hello
from predictfilm.views import clea
from predictfilm.views import current_datetime
from predictfilm.views import cleantha
from predictfilm.views import parseExcel
from predictfilm.views import renderresponse
from predictfilm.views import models
from predictfilm.views import deleteModel
from predictfilm.views import d3Show
from predictfilm.views import boxOffice
from predictfilm.views import index
from predictfilm.views import boxOfficeFilter
from predictfilm.views import sinaSpider
from predictfilm.views import sinaRsaSpider
from predictfilm.views import readExcel
from predictfilm.views import movieSpider
from predictfilm.views import getDate
from predictfilm.views import weekSpider
from predictfilm.views import filterBoxOffice
from predictfilm.views import weekBoxOffice
from predictfilm.views import diagram
from predictfilm.views import navi

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'filepredict.views.home', name='home'),
    # url(r'^filepredict/', include('filepredict.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', hello),
    url(r'^$', index),
    url(r'^datetime/$', current_datetime),
    url(r'^another_datetime/$', current_datetime),
    url(r'^cleantha/$', cleantha),
    url(r'^parsexcel/$', parseExcel),
    url(r'^renres/$', renderresponse),
    url(r'^models/$', models),
    url(r'^delete/$', deleteModel),
    url(r'^d3/$', d3Show),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH}),
    url(r'^bootstrap/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.BOOTSTRAP_PATH}),
    url(r'^boxoffice/$', boxOffice),
    url(r'^cleantha/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CLEANTHA_PATH}),
    url(r'^boxofficefilter/$', boxOfficeFilter),
    url(r'^spider/$', sinaSpider),
    url(r'^rsaspider/$', sinaRsaSpider),
    url(r'^readexcel/$', readExcel),
    url(r'^moviespider/$', movieSpider),
    url(r'^getdate/$', getDate),
    url(r'^weekspider/$', weekSpider),
    url(r'^filterboxoffice/$', filterBoxOffice),
    url(r'^weekboxoffice/$', weekBoxOffice),
    url(r'^diagram/$', diagram),
    url(r'^navi/$', navi),
)
