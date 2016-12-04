# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, render_to_response, get_object_or_404

from django.template import Context, Template, RequestContext
from django.template.loader import get_template

from meta.models import *
from serializers import *

from deft.settings import APP_SETTINGS
from deft.settings import RUNNING_DEVSERVER
from deft.settings import STATIC_LOCATION

def home(request):
    tname	= request.GET.get('template', APP_SETTINGS['deft.home']['default_template']) # template name minus ".html"

    c = Context(
        {
            'title'	: 'DEFT HOME',
            'server'	: request.META['SERVER_NAME'],
            'port'	: request.META['SERVER_PORT'],
            'static'	: STATIC_LOCATION,
            'my_name'	: 'mxp'
            }
        )
    

    return render_to_response(tname+'.html', c)
