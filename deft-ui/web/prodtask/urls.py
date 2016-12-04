from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^prodtask_table/$', 'prodtask.views.prodtask_table', name='prodtask_table'),
    url(r'^prodtask_tabledata/$', 'prodtask.views.prodtask_tabledata', name='prodtask_table_data'),
    url(r'^prodtask_about/$', 'prodtask.views.about', name='about'),
    url(r'^$', 'prodtask.views.home', name='home'),

)
