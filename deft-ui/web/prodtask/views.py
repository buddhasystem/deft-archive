# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, render_to_response
from django.template import Context, Template, RequestContext
from django.template.loader import get_template

from models import ProdTask

from core.datatable import datatable_entry, datatable_data_answer

def home(request):
    tmpl = get_template('prodtask/_index.html')
    c = Context( {'title'  : 'ProdTask Monitoring'} )
    return HttpResponse(tmpl.render(c))

def about(request):
    tmpl = get_template('prodtask/_about.html')
    c = Context( {'title'  : 'ProdTasks about',} )
    return HttpResponse(tmpl.render(c))

##    reqid = models.BigIntegerField(primary_key=True, db_column='REQID') # Field name made lowercase.
##
##    swrelease = models.CharField(max_length=20, db_column='SWRELEASE')
##    lparams = models.CharField(max_length=22, db_column='LPARAMS')
##    ppstate = models.CharField(max_length=12, db_column='PPSTATE')
##
##    parent_id = models.IntegerField(null=True, db_column='PARENT_TID', blank=True)
##    bug_report = models.IntegerField(null=True, db_column='BUG_REPORT', blank=True)
##    cpu_per_event = models.IntegerField(null=True, db_column='CPUPEREVENT', blank=True)
##    first_inputfile_n = models.IntegerField(null=True, db_column='FIRST_INPUTFILE_N', blank=True)
##    phys_group = models.CharField(max_length=22, db_column='PHYS_GROUP')
##    ctag = models.CharField(max_length=12, db_column='CTAG')
##    bug_reference = models.IntegerField(null=True, db_column='BUG_REFERENCE', blank=True)
##
##    BUG_REFERENCE = models.IntegerField(null=True,db_column="BUG_REFERENCE",max_length=22)
##    LASTMODIFIED  = models.DateTimeField(db_column="LASTMODIFIED",max_length=7)
##    DSN = models.CharField( db_column="DSN",max_length=15)
##    PRODSTEP= models.CharField(db_column="PRODSTEP",max_length=40)
##    TRF= models.CharField(db_column="TRF",max_length=80)
##    TRFV=models.CharField(db_column="TRFV",max_length=40)
##    email=models.CharField(db_column="email",max_length=60)
##    memory= models.IntegerField(null=True,db_column="memory",max_length=22)
##    CONFIGURATION_TAG= models.CharField(db_column="CONFIGURATION_TAG",max_length=30)
##    TOTAL_AVAIL_JOBS=  models.IntegerField(db_column="TOTAL_AVAIL_JOBS",max_length=22)
##    TIDTYPE = models.CharField(null=True, "TIDTYPE",max_length=12)
##    INPUTDATASET = models.CharField(db_column="INPUTDATASET",max_length=150)
##    taskname= models.CharField(db_column="taskname",max_length=130)
##    VPARAMS= models.CharField(db_column="VPARAMS",max_length=4000)
##    TOTAL_F_EVENTS= models.IntegerField(null=True, db_column="TOTAL_F_EVENTS",max_length=22)
##    FORMATS=  models.CharField(db_column="FORMATS",max_length=256)
##    TOTAL_REQ_JOBS= models.IntegerField(null=True,  db_column="TOTAL_REQ_JOBS",max_length=22)
##    TOTAL_DONE_JOBS= models.IntegerField(null=True, db_column="TOTAL_DONE_JOBS",max_length=22)
##    POSTPRODUCTION=  models.CharField( db_column="POSTPRODUCTION",max_length=128)
##    TOTAL_INPUT_FILES = models.IntegerField(null=True,  db_column="TOTAL_INPUT_FILES",max_length=22)
##    TRF_CACHE = models.IntegerField(null=True, db_column= "EVENTS_PER_FILE",max_length=22)
##    TRF_CACHE=  models.CharField(db_column="TRF_CACHE",max_length=30)
##    status =  models.CharField(db_column="status",max_length=12)
##    PHYS_REF = models.CharField(db_column="PHYS_REF",max_length=65)
##    PRODTAG =  models.CharField( db_column="PRODTAG",max_length=50)

prodtask_table_meta = {'fields' : [
                               { 'aname' : 'reqid',  'sortdir':	[ 'desc', 'asc' ],           'tname' : 'id',             'display_name' : 'ID' },
                               { 'aname' : 'taskname',            'tname' : 'taskname',              'display_name' : 'Task name' },
                         #      { 'aname' : 'start_time',       'tname' : 'start_time',    'display_name' : 'Start time' },
                               { 'aname' : 'TOTAL_REQ_JOBS',    'tname' : 'reqjobs',                'display_name' : 'REQ JOBS' },
                               { 'aname' : 'TOTAL_DONE_JOBS',    'tname' : 'donejobs',               'display_name' : 'DONE JOBS' },
                               { 'aname' : 'status',          'tname' : 'status',       'display_name' : 'State' },
                               { 'aname' : 'TOTAL_F_EVENTS',       'tname' : 'events',    'display_name' : 'Events' },
                               { 'aname' : 'priority',       'tname' : 'priority',    'display_name' : 'Priority' },
                               { 'aname' : 'INPUTDATASET',       'tname' : 'input',    'display_name' : 'Input' },
                             ],
                       'title'  : 'Requested ProdTasks',
                       'URL'    : 'prodtask:prodtask_table_data' ,
                       'sorting': [[0,'desc']],
                       'length_list' : [ [ 10, 500, 1000], [ 10, 500, 1000] ],
                       'length_display' : 10,
                       'row_type': 'object',
                       'row_call_back': """
                       function( nRow, aData, iDisplayIndex, iDisplayIndexFull )
                       {
                            $('td:eq(0)', nRow).html('<a href="http://pandamon.cern.ch/jobinfo?jobtype=production&taskID='+aData.id+'">'+aData.id+'</a>');
                            $('td:eq(1)', nRow).html('<a href="http://panda.cern.ch/?mode=showtask0&reqid='+aData.id+'">'+aData.taskname+'</a>');
                            $('td:eq(2)', nRow).css('text-align','right');
                            if( aData.donejobs != 0 )
                                $('td:eq(3)', nRow).html('<a href="http://pandamon.cern.ch/jobinfo?jobStatus=finished,failed,cancelled&limit=200&hours=96&taskID='+aData.id+'">'+aData.donejobs+'</a>');
                            $('td:eq(7)', nRow).html('<a href="http://panda.cern.ch/?mode=dset&name='+aData.input+'">'+aData.input+'</a>');
                        }""",
                        }

def prodtask_table(request):
    return datatable_entry(request, prodtask_table_meta, 'core/_datatable.html', 'prodtask/_index.html')

def prodtask_tabledata(request):
    return datatable_data_answer(request, prodtask_table_meta, ProdTask, 'grisli')

