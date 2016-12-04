from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^mcprod_requests_table/$', 'mcprod.views.mcprod_requests_table', name='requests_table'),

    url(r'^mcprod_about$', 'mcprod.views.about', name='about'),
    url(r'^$', 'mcprod.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
