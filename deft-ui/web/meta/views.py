###
### The DEFT UI Meta-Task and Task pages
###
try:
    import simplejson
except:
    import json as simplejson

from django			import forms
from django.http		import HttpResponse, HttpResponseRedirect
from django.shortcuts		import render, render_to_response, get_object_or_404
from django.template		import Context, Template, RequestContext
from django.template.loader	import get_template
from django.core.paginator	import Paginator, EmptyPage, PageNotAnInteger

from meta.models		import *
from serializers		import *
from dbtools			import *

### a few utility-type setting for easier configuration:
from deft.settings		import APP_SETTINGS
from deft.settings		import RUNNING_DEVSERVER
from deft.settings		import STATIC_LOCATION

###
### Meta-Task Monitor
def meta(request):
    tname	= request.GET.get('template', APP_SETTINGS['meta.meta']['default_template']) # template name minus ".html"
    metaID	= request.GET.get('meta', '')
    frm		= request.GET.get('format', 'html') # The format is either "json", or "html" (default)
    sortBy	= request.GET.get('sort', 'id')

    page	= int(request.GET.get('page', '1'))
    NperPage	= int(request.GET.get('N', '5'))

    metas = []

    if metaID=='':
        if sortBy == 'id':
            metas = MetaTask.objects.exclude(meta_state='template').order_by('meta_id')
        elif sortBy == 'manager':
            metas = MetaTask.objects.exclude(meta_state='template').order_by('meta_manager')
        elif sortBy == 'requestor':
            metas = MetaTask.objects.exclude(meta_state='template').order_by('meta_requestor')
        else:
            metas = MetaTask.objects.exclude(meta_state='template').order_by('meta_id') # catch all

    else:
        metas = MetaTask.objects.filter(meta_id=int(metaID))

    paginator = Paginator(metas, NperPage)

    try:			# don't forget to import exceptions from the paginator module
        toShow = paginator.page(page)
    except PageNotAnInteger:	# If page is not an integer, deliver first page.
        toShow = paginator.page(1)
    except EmptyPage:		# If page is out of range (e.g. 9999), deliver last page of results.
        toShow = paginator.page(paginator.num_pages)

    if toShow.has_previous:
        previousPage=toShow.previous_page_number
    else:
         previousPage=1

    if toShow.has_next:
        nextPage=toShow.next_page_number
    else:
        nextPage=1000000

    c = RequestContext(request,
        {
            'title'	: 'DEFT Meta-Task Monitor',
            'server'	: request.META['SERVER_NAME'], 'port'	: request.META['SERVER_PORT'],
            'static'	: STATIC_LOCATION,            'my_name'	: 'Test User', "metas"	: toShow,
            'previous'	: previousPage,			'next'	: nextPage,
            'sortclause': '&sort='+sortBy
            }
        )

    if frm == 'json':
        return HttpResponse(serializeObjArray(metas))
    else:
        return render_to_response(tname+'.html', c)

    # Dev notes:
    # Crude debug: for m in metas:#    print m.meta_id
    # Add to the dict for debugging POST:'answer' : request.method,
    #
###
def editmeta(request):
    tname	= request.GET.get('template', APP_SETTINGS['meta.editmeta']['default_template']) # template name minus ".html"
    metaID	= request.GET.get('meta', '')

    metas = []

    if metaID=='':
        metas = MetaTask.objects.all()
    else:
        metas = MetaTask.objects.filter(meta_id=int(metaID))

    c = RequestContext(request,
        {
            'title'	: 'DEFT Meta-Task Editor',
            'server'	: request.META['SERVER_NAME'], 'port'	: request.META['SERVER_PORT'],
            'static'	: STATIC_LOCATION,
            'my_name'	: 'Test User',
            "metas"	: metas
            }
        )
    
    return render_to_response(tname+'.html', c)

###
def metadetail(request):
    tname	= request.GET.get('template', APP_SETTINGS['meta.metadetail']['default_template']) # template name minus ".html"
    metaID	= request.GET.get('meta', '')
    alter	= request.GET.get('alter', '')

    metas = []
    tasks = []

    if metaID!='':
        metas = MetaTask.objects.filter(meta_id=int(metaID))

    a = 'ok '
    m = {}
    try:
        m = metas[0]
        if alter !='': # there was a command we need to handle
            parsedCommand = simplejson.loads(alter)
            for k in parsedCommand.keys():
                setattr(m, k, parsedCommand[k])
                a+=str(k)+':'+parsedCommand[k]+' '
            m.save()
    except:
        pass

    if metaID!='':
        tasks = Task.objects.filter(task_meta=int(metaID)).order_by('task_id')

    c = RequestContext(request,
        {
            'title'	: 'DEFT Meta-Task Display', 'static' : STATIC_LOCATION, 'my_name' : 'Test User',
            'server'	: request.META['SERVER_NAME'], 'port'	: request.META['SERVER_PORT'],
            "m"		: m, "tasks" : tasks,
            "answer"	: a
            }
        )
    
    return render_to_response(tname+'.html', c)


### Meta-Task Creation
def newmeta(request):
    tname	= request.GET.get('template', APP_SETTINGS['meta.meta']['default_template']) # template name minus ".html"
    templateID	= request.GET.get('template', '')

    s = 'no template'

    if templateID!='':
        m = MetaTask.objects.get(pk=int(templateID))
        try:
            new_meta_id = getSeq()
            m.pk=new_meta_id
            s=m.meta_state
            m.meta_state="disarmed"
            m.meta_template=templateID
            m.save()

            tasks = Task.objects.filter(task_meta=int(templateID)).order_by('task_id')
            first = True
            for t in tasks:
                if first==True:
                    t.pk=new_meta_id
                    first=False
                else:
                    t.pk=getSeq()
                t.task_meta=new_meta_id
                t.task_state="disarmed"
                t.save()

        except:
            pass

    return HttpResponse(str(s))

###
def taskdetail(request):
    tname	= request.GET.get('template', APP_SETTINGS['meta.taskdetail']['default_template']) # template name minus ".html"
    taskID	= request.GET.get('task', '')
    alter	= request.GET.get('alter', '')

    tasks = []

    if taskID!='':
        tasks = Task.objects.filter(task_id=int(taskID))

    a = 'ok'
    t = {}
    try:
        t = tasks[0]
        if alter !='': # there was a command we need to handle
            parsedCommand = simplejson.loads(alter)
            for k in parsedCommand.keys():
                setattr(t, k, parsedCommand[k])
            t.save()
    except:
        pass

    c = RequestContext(request,
        {
            'title'	: 'DEFT Task Display', 'static' : STATIC_LOCATION, 'my_name' : 'Test User',
            'server'	: request.META['SERVER_NAME'], 'port'	: request.META['SERVER_PORT'],
            "t"		: t,
            "answer"	: a
            }
        )
    
    return render_to_response(tname+'.html', c)

###
def lib(request):
    tname	= request.GET.get('template', APP_SETTINGS['meta.lib']['default_template']) # template name minus ".html"
    metaID	= request.GET.get('meta', '')
    frm		= request.GET.get('format', 'html') # The format is either "json", or "html" (default)

    metas = []

    if metaID=='':
        metas = MetaTask.objects.filter(meta_state='template').order_by('meta_id')
    else:
        metas = MetaTask.objects.filter(meta_id=int(metaID))

    # Crude debug: for m in metas:#    print m.meta_id
    # Add to the dict for debugging POST:'answer' : request.method,

    c = RequestContext(request,
        {
            'title'	: 'DEFT Meta-Task Monitor',
            'server'	: request.META['SERVER_NAME'], 'port'	: request.META['SERVER_PORT'],
            'static'	: STATIC_LOCATION,            'my_name'	: 'Test User', "metas"	: metas
            }
        )

    if frm == 'json':
        return HttpResponse(serializeObjArray(metas))
    else:
        return render_to_response(tname+'.html', c)

###
### Task Monitor
def task(request):
    frm		= request.GET.get('format', 'html') # can also be "json"
    tname	= request.GET.get('template', APP_SETTINGS['meta.task']['default_template']) # template name minus ".html"

    page	= int(request.GET.get('page', '1'))
    NperPage	= int(request.GET.get('N', '10'))
    sortBy	= request.GET.get('sort', 'id')

    taskID	= request.GET.get('task', '')
    metaID	= request.GET.get('meta', '')

    # print 't', taskID,'m', metaID

    tasks = []

    if taskID=='':
        tasks = Task.objects.all().exclude(task_state='template').order_by('task_id')
    elif taskID!='':
        tasks = Task.objects.filter(task_id=int(taskID)).exclude(task_state='template')

    if metaID!='':
        tasks = Task.objects.filter(task_meta=int(metaID)).exclude(task_state='template')

    task_count = len(tasks)
 
    paginator = Paginator(tasks, NperPage)

    try:			# don't forget to import exceptions from the paginator module
        toShow = paginator.page(page)
    except PageNotAnInteger:	# If page is not an integer, deliver first page.
        toShow = paginator.page(1)
    except EmptyPage:		# If page is out of range (e.g. 9999), deliver last page of results.
        toShow = paginator.page(paginator.num_pages)

    if toShow.has_previous:
        previousPage=toShow.previous_page_number
    else:
         previousPage=1

    if toShow.has_next:
        nextPage=toShow.next_page_number
    else:
        nextPage=1000000

   
    c = RequestContext(request,
        {
            'title'	: 'DEFTTask Monitor',
            'server'	: request.META['SERVER_NAME'], 'port'	: request.META['SERVER_PORT'],
            'static'	: STATIC_LOCATION,            'my_name'	: 'Test User', "tasks"	: toShow,
            'previous'	: previousPage,			'next'	: nextPage,
            'sortclause': '&sort='+sortBy
            }
        )

    
    if frm == 'json':
        return HttpResponse(serializeObjArray(tasks))
    else:
        return render_to_response(tname+'.html', c)

### Object Deletion
def delete(request):
    taskID	= request.GET.get('task', '')
    metaID	= request.GET.get('meta', '')

    if metaID!='':
        try:
            m = MetaTask.objects.get(pk=int(metaID))
            m.delete()
        except:
            pass
        return HttpResponse('Meta-Task '+metaID+' deleted')

    if taskID!='':
        try:
            t = Task.objects.get(pk=int(taskID))
            t.delete()
        except:
            pass
        return HttpResponse('Task '+taskID+' deleted')


###
def help(request):
    tname	= request.GET.get('template', APP_SETTINGS['meta.help']['default_template']) # template name minus ".html"

    c = Context(
        {
            'title'	: 'DEFT Help',
            'server'	: request.META['SERVER_NAME'],
            'port'	: request.META['SERVER_PORT'],
            'static'	: STATIC_LOCATION,
            'my_name'	: 'mxp'
            }
        )
    

    return render_to_response(tname+'.html', c)
###
def debug(request):
    s = getSeq()
    return HttpResponse(str(s))


###
### ATTENTION - the method below is for rapid prototyping and it mocks up the data in the dictionary
### instead of accessing DB, for extra flexibility. Don't use in any application and don't bookmark
def mock_meta(request):

    tmpl = get_template('deft_meta_1.html')

    metas = []
    info = [
	{
            'meta_id':'11312',
            'meta_name':'mc13.8TeV.Pythia.Ztautau332',
            'meta_template':'187',
            'meta_state':'Running',
            'meta_req_ts':'2013-09-03 18:07',
            'meta_upd_ts':'2013-09-04 07:02'
            },
	{
            'meta_id':'11315',
            'meta_name':'mc13.8TeV.Pythia.Ztautau337',
            'meta_template':'187',
            'meta_state':'Running',
            'meta_req_ts':'2013-09-03 19:01',
            'meta_upd_ts':'2013-09-04 08:12'
            },
	{
            'meta_id':'11316',
            'meta_name':'mc13.8TeV.Pythia.Ztautau338',
            'meta_template':'187',
            'meta_state':'On hold',
            'meta_req_ts':'2013-09-03 19:17',
            'meta_upd_ts':'2013-09-04 09:21'
            },
	{
            'meta_id':'11319',
            'meta_name':'mc13.8TeV.Pythia.Wmunu115',
            'meta_template':'203',
            'meta_state':'Running',
            'meta_req_ts':'2013-09-11 11:13',
            'meta_upd_ts':'2013-09-12 13:26'
            },
	{
            'meta_id':'11778',
            'meta_name':'nightly.SL6.build',
            'meta_template':'011',
            'meta_state':'Cancelled',
            'meta_req_ts':'2013-09-10 00:01',
            'meta_upd_ts':'2013-09-10 01:02'
            },
	{
            'meta_id':'11322',
            'meta_name':'mc13.8TeV.Pythia.AlpgenJ121',
            'meta_template':'081',
            'meta_state':'Running',
            'meta_req_ts':'2013-09-01 00:02',
            'meta_upd_ts':'2013-09-02 01:22'
            }
	]

    for d in info:
	metas.append(d)

    return render_to_response('deft_meta_1.html', {'my_name': 'mxp', 'title' : 'DEFT Meta-Task Monitor', 'metas': metas})


    # Keep that for a while for reference -- this is how we detect POST in handling
    # simple forms with radio buttons
    # try:
    #     if request.method == 'POST':
    #         a='foo'
    #         x = request.POST.get('choice')
    #         if x != None:
    #             a+=str(x)
    #         c = RequestContext(request, {'answer': a})
    #         return render_to_response(tname+'.html', c)
    # except:
    #     pass
