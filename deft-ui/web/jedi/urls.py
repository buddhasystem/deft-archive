from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^jeditask_table/$', 'jedi.views.jeditask_table', name='task_table'),
    url(r'^jeditask_tabledata/$', 'jedi.views.jeditask_tabledata', name='task_table_data'),

    url(r'^jedidataset_table/$', 'jedi.views.jedidataset_table', name='dataset_table'),
    url(r'^jedidataset_tabledata/$', 'jedi.views.jedidataset_tabledata', name='dataset_table_data'),

    url(r'^jedidatasetcontent_table/$', 'jedi.views.jedidatasetcontent_table', name='datasetcontent_table'),
    url(r'^jedidatasetcontent_tabledata/$', 'jedi.views.jedidatasetcontent_tabledata', name='datasetcontent_table_data'),

    url(r'^jedi_about$', 'jedi.views.about', name='about'),
    url(r'^$', 'jedi.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
