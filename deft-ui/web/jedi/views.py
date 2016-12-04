# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, render_to_response
from django.template import Context, Template, RequestContext
from django.template.loader import get_template

from models import JEDITask, JEDIDataset, JEDIDatasetContent

from core.datatable import datatable_entry, datatable_data_answer


def home(request):
    tmpl = get_template('jedi/_index.html')
    c = Context( {'title'  : 'JEDI Monitoring Home'} )
    return HttpResponse(tmpl.render(c))

def about(request):
    tmpl = get_template('jedi/_about.html')
    c = Context( {'title'  : 'JEDI Monitoring about',} )
    return HttpResponse(tmpl.render(c))


##        jeditaskid		= models.DecimalField(decimal_places=0, max_digits=12, db_column='JEDITASKID', primary_key=True)
##        taskname        = models.CharField(max_length=128,  db_column='TASKNAME', blank=True)
##        status          = models.CharField(max_length=64, db_column='STATUS', blank=True)
##        username        = models.CharField(max_length=128, db_column='USERNAME', blank=True)
##        vo	            = models.CharField(max_length=16,  db_column='VO', blank=True)
##        creationdate	= models.DateTimeField(db_column='CREATIONDATE')
##        modificationtime		= models.DateTimeField(db_column='MODIFICATIONTIME')

jeditask_table_meta = {'fields' : [
                               { 'width': '70%','searchable': 'false', 'sortable': 'false', 'aname' : 'jeditaskid',        'tname' : 'jeditaskid',         'display_name' : 'JEDITask ID' },
                               { 'aname' : 'taskname',          'tname' : 'taskname',           'display_name' : 'Task name' },
                               { 'sortable': 'false', 'aname' : 'status',            'tname' : 'status',             'display_name' : 'Status' },
                               { 'searchable': 'false', 'aname' : 'username',          'tname' : 'username',           'display_name' : 'Username' },
                               { 'sortable': 'false', 'aname' : 'vo',                'tname' : 'vo',                 'display_name' : 'VO' },
                               { 'searchable': 'false', 'aname' : 'creationdate',      'tname' : 'creationdate',       'display_name' : 'Creation date' },
                               { 'aname' : 'modificationtime',  'tname' : 'modificationtime',   'display_name' : 'Modification time' },
                             ],
                       'title'  : 'JEDI Tasks',
                       'URL'    : 'jedi:task_table_data',
                       'row_type': 'object'
                        }

def jeditask_table(request):
    return datatable_entry(request, jeditask_table_meta, 'core/_datatable.html', 'jedi/_index.html')

def jeditask_tabledata(request):
    return datatable_data_answer(request, jeditask_table_meta, JEDITask)



##        jeditaskid		= models.ForeignKey(JEDITask)
##        datasetid		= models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASETID', primary_key=True)
##        datasetname     = models.CharField(max_length=128,  db_column='TASKNAME', blank=True)
##        status          = models.CharField(max_length=64, db_column='STATUS', blank=True)
##        site            = models.CharField(max_length=128, db_column='SITE', blank=True)
##        nevents            = models.CharField(max_length=128, db_column='NEVENTS', blank=True)
##        vo	            = models.CharField(max_length=16,  db_column='VO', blank=True)
##        creationdate	= models.DateTimeField(db_column='CREATIONDATE')
##        modificationtime		= models.DateTimeField(db_column='MODIFICATIONTIME')

jedidataset_table_meta = {'fields' : [
                               { 'aname' : 'jeditask__jeditaskid',  'tname' : 'jeditaskid',         'display_name' : 'JEDITask id' },
                               { 'sortable': 'false','aname' : 'jeditask__username',    'tname' : 'username',           'display_name' : 'Username' },
                               { 'searchable': 'false', 'aname' : 'datasetid',             'tname' : 'datasetid',          'display_name' : 'JEDIDataset id' },
                               { 'aname' : 'datasetname',           'tname' : 'datasetname',        'display_name' : 'Dataset name' },
                               { 'aname' : 'status',                'tname' : 'status',             'display_name' : 'Status' },
                            #   { 'aname' : 'site',                  'tname' : 'site',               'display_name' : 'Site' },
                            #   { 'aname' : 'nevents',               'tname' : 'nevents',            'display_name' : 'NEvents' },
                               { 'sortable': 'false', 'searchable': 'false', 'aname' : 'vo',                    'tname' : 'vo',                 'display_name' : 'VO' },
                               { 'aname' : 'creationdate',          'tname' : 'creationdate',       'display_name' : 'Creation date' },
                               { 'aname' : 'modificationtime',      'tname' : 'modificationtime',   'display_name' : 'Modification time' },
                             ],
                       'title'  : 'JEDI Datasets',
                       'URL'    : 'jedi:dataset_table_data' ,
                       'row_type': 'object'
                        }

def jedidataset_table(request):
    return datatable_entry(request, jedidataset_table_meta, 'core/_datatable.html', 'jedi/_index.html')

def jedidataset_tabledata(request):
    return datatable_data_answer(request, jedidataset_table_meta, JEDIDataset)



##    dataset		   = models.ForeignKey(JEDIDataset, db_column='DATASETID')
##    fileid          = models.CharField(max_length=128,  db_column='TASKNAME', blank=True)
##    status          = models.CharField(max_length=64, db_column='STATUS', blank=True)
##    fsize           = models.CharField(max_length=128, db_column='FSIZE', blank=True)
##    lfn             = models.CharField(max_length=128, db_column='LFN', blank=True)
##    guid	        = models.CharField(max_length=16,  db_column='GUID', blank=True)
##    creationdate	= models.DateTimeField(db_column='CREATIONDATE')
##    lastattempttime		= models.DateTimeField(db_column='LASTATTEMPTTIME')

jedidatasetcontent_table_meta = {'fields' : [
                               { 'width': '500px', 'searchable': 'false', 'aname' : 'dataset__jeditask__jeditaskid',  'tname' : 'jeditaskid',         'display_name' : 'JEDITask id' },
                               { 'sortable': 'false',   'aname' : 'dataset__jeditask__username',    'tname' : 'username',           'display_name' : 'Username' },
                               { 'searchable': 'false','aname' : 'dataset__datasetid',             'tname' : 'datasetid',          'display_name' : 'JEDIDataset id' },
                               { 'aname' : 'dataset__datasetname',           'tname' : 'datasetname',        'display_name' : 'Dataset name' },
                               { 'aname' : 'fileid',                'tname' : 'fileid',             'display_name' : 'File id' },
                               { 'aname' : 'status',                'tname' : 'status',             'display_name' : 'Status' },
                               { 'aname' : 'fsize',                 'tname' : 'fsize',              'display_name' : 'File size' },
                               { 'aname' : 'lfn',                   'tname' : 'lfn',                'display_name' : 'LFN' },
                               { 'aname' : 'guid',                  'tname' : 'guid',               'display_name' : 'GUID' },
                               { 'aname' : 'creationdate',          'tname' : 'creationdate',       'display_name' : 'Creation date' },
                               { 'aname' : 'lastattempttime',       'tname' : 'lastattempttime',    'display_name' : 'Last attempt time' },
                             ],
                       'title'  : 'JEDI Dataset contents',
                       'URL'    : 'jedi:datasetcontent_table_data' ,
                       'row_type': 'object'
                        }

def jedidatasetcontent_table(request):
    return datatable_entry(request, jedidatasetcontent_table_meta, 'core/_datatable.html', 'jedi/_index.html')

def jedidatasetcontent_tabledata(request):
    return datatable_data_answer(request, jedidatasetcontent_table_meta, JEDIDatasetContent)

