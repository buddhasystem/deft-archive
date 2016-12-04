from django.conf.urls import patterns, include, url
from meta.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',			'deft.views.home'),
    url(r'^task/$',		'meta.views.task'),
    url(r'^meta/$',		'meta.views.meta'),
    url(r'^editmeta/$', 	'meta.views.editmeta'),
    url(r'^newmeta/$', 		'meta.views.newmeta'),
    url(r'^delete/$', 		'meta.views.delete'),
    url(r'^metadetail/$', 	'meta.views.metadetail'),
    url(r'^taskdetail/$', 	'meta.views.taskdetail'),
    url(r'^lib/$',		'meta.views.lib'),
    url(r'^help/$',		'meta.views.help'),
    url(r'^debug/$',		'meta.views.debug'),
#
    url(r'^mock_meta/$',	'meta.views.mock_meta'),
    url(r'^taskCreate/$',	'groupInterface.views.taskCreate'),
    url(r'^metaCreate/$',	'groupInterface.views.metaCreate'),

    url(r'^jedi/', include('jedi.urls', namespace='jedi')),
    url(r'^prodtask/', include('prodtask.urls', namespace='prodtask')),
    url(r'^mcprod/', include('mcprod.urls', namespace='mcprod')),

    #url(r'^home/$', home, name='home'),
    #url(r'^$', 'groupInterface.views.home', name='home'),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
