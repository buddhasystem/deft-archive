# Create your views here.
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, render_to_response
from django.template import Context, Template, RequestContext
from django.template.loader import get_template

from core.datatable import datatable_entry, datatable_data_answer

from deft.settings		import APP_SETTINGS

import gspread
from datetime import datetime

import json
import urllib2


def home(request):
    tmpl = get_template('mcprod/_index.html')
    c = Context( {'title'  : 'Monte Carlo Production Home'} )
    return HttpResponse(tmpl.render(c))

def about(request):
    tmpl = get_template('mcprod/_about.html')
    c = Context( {'title'  : 'Monte Carlo Production about',} )
    return HttpResponse(tmpl.render(c))

mcprod_requests_table_meta = {'fields' : [
               #                { 'searchable': 'false',  'aname' : 'id',        'tname' : 'id',         'display_name' : '' },
                               { 'aname' : 'slice',     'tname' : 'slice',           'display_name' : 'Slice' },
                               { 'aname' : 'description', 'tname' : 'description',           'display_name' : 'Description' },
                               { 'aname' : 'type',        'tname' : 'type',                 'display_name' : 'Type' },
                               { 'aname' : 'approval',      'tname' : 'approval',       'display_name' : 'Approval' },
                               { 'aname' : 'manager',  'tname' : 'manager',   'display_name' : 'Manager' },
                               { 'aname' : 'spreadsheet',  'tname' : 'spreadsheet',   'display_name' : 'Spreadsheet' },
                               { 'aname' : 'panda',  'tname' : 'panda',   'display_name' : 'Panda' },
                               { 'aname' : 'status',            'tname' : 'status',             'display_name' : 'Status' },
                             ],
                       'title'  : 'List of Production Requests',
                       'URL'    : 'mcprod:requests_table_data',
                       'row_type': 'array',
                       'no_individual_search': 'true',
                        }



def get_data():
    processing = ['evgen', 'simul', 'recon', 'merge']
    states = ['submitting', 'failed', 'aborted', 'waiting']

    stasus_file = APP_SETTINGS['mcprod.files']['status_json']

    # Get dictionary containing the last saved status of the requests
   # with open(stasus_file) as fcsv:
  #      content = fcsv.readlines()

    f=urllib2.urlopen(stasus_file)
    content = f.readlines()

    # Create a dictionary with the status
    panda_details = {}
    for dataset in content:
        data = eval(dataset)
        panda_details[data['url']] = data

    #panda_links_file = APP_SETTINGS['mcprod.files']['panda_links']

    # File to save links for tasks which status should be checked
    #f = open(panda_links_file,'w')

    now = datetime.now()

    guser = APP_SETTINGS['mcprod.auth']['user']
    gpasswd = APP_SETTINGS['mcprod.auth']['password']

    gc = gspread.login(guser,gpasswd)

    # If you want to be specific, use a key (which can be extracted from
    # the spreadsheet's url)
    sh = gc.open_by_key('0AiEl32nvxJogdFhsbmRnNk80bm9qS29tTWhhSXdlVVE')

    # Most common case: Sheet1
    worksheet = sh.sheet1

    # Get content of ALL cells in spreadsheet
    list_of_lists = worksheet.get_all_values()

    i = 0
    objs = []
    # Loop over the rows in excel spreadsheet
    for row in list_of_lists :
        obj = []
        if i == 0 :
            # Header of Table for DataTable class
            details = '{ "sTitle": "" },'+'{ "sTitle": "'+str(row[0]).rstrip('\r\n')+'" },'+'{ "sTitle": "'+str(row[1]).rstrip('\r\n')+'" },'+'{ "sTitle": "'+str(row[2]).rstrip('\r\n')+'" },'+'{ "sTitle": "'+str(row[3]).rstrip('\r\n')+'" },'+'{ "sTitle": "'+str(row[4]).rstrip('\r\n')+'" },'+'{ "sTitle": "'+str(row[5]).rstrip('\r\n')+'" }'+',{ "sTitle": "Panda" }'+',{ "sTitle": "Status" }'
        status_details = '<center>Unknown</center>'

        if i != 0 and len(str(row[0])) > 1 :
            isOld = 0

            # Check Approval column
            if len(str(row[3])) < 2 :
                status = 'Pending'
            else :
                status = str(row[3]).rstrip('\r\n')
                if len(status) == 10 and '/' in status :
                    isOld = int((now - datetime.strptime(status,'%d/%m/%Y')).days)

            # Request spreadsheet link if exists
            if len(row[5]) > 4 :
                href = '<a href="'+str(row[5]).rstrip('\r\n')+'">'+str(row[5]).rstrip('\r\n')+'</a>'
            else:
                href = str(row[5]).rstrip('\r\n')

            # Request panda link if exists
            if len(row[17]) > 4 :
                this_url = str(row[17]).rstrip('\r\n')
                prod = '<a href="'+this_url+'"> link </a>'

                # If link check if the panda link exists
                # will save panda link in file (to be checked) if :
                #     1 status does not exists for the task and task is not too old
                #     2 status exists but task did finished
                if ( len(this_url) == 19 or len(this_url) == 20 ) and isOld < 100 :
                    if this_url not in panda_details :
                       # f.write(this_url+"\n")
                       pass
                    else :
                        recon = panda_details[this_url]['recon']
                        evgen = panda_details[this_url]['evgen']
                        if int(recon[0]*0.95) > int(recon[1]) or int(evgen[0]*0.95) > int(evgen[1]) or int(recon[0]) == 0 :
                           # f.write(this_url+"\n")
                           pass

                # Create the progress bars for status
                if this_url in panda_details :
                    status_details = '<div style="display: inline-block; width: 180px; height: 30px">'
                    data = panda_details[this_url]
                    for ptype in processing :
                        arr = data[ptype]
                        if arr[0] > 0 :
                            val = int(100.*float(arr[1])/float(arr[0]))
                        else :
                            val = 0
                        status_details += '<div class="meter '+ptype+'" title="'+ptype+' : '+str(arr[1])+'/'+str(arr[0])+'"> <span style="width: '+str(val)+'%"></span></div>'
                    status_details += '</div><div style="width:180px;postion:relative;margin: 2px 2px 2px 2px">'
                    for st in states :
                        status_details += st + " : " + str(data[st])+ "  "
                    status_details += "</div>"

            else:
                prod = str(row[17]).rstrip('\r\n')

            # Save the information in the array for DataTable
          #  print "['"+str(i+1)+"','"+str(row[0]).rstrip('\r\n')+"','"+(str(row[1]).rstrip('\r\n')).replace("'", "prime")+"','"+str(row[2]).rstrip('\r\n')+"','"+status+"','"+str(row[4]).rstrip('\r\n')+"','"+href+"','"+prod+"','"+status_details+"'],"
            obj =  [ row[0] , row[1], row[2], status, row[4], href , prod , status_details ]

            objs.append(obj)
        i=i+1

    return objs


def mcprod_requests_table(request):

    objs = get_data()

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else str(obj)

    mcprod_requests_table_meta['data'] = json.dumps(objs, ensure_ascii=False, default=dthandler)

    return datatable_entry(request, mcprod_requests_table_meta, 'core/_datatable.html', 'mcprod/_index.html')





