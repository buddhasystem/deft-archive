from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, render_to_response
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.db.models import Q

from datetime import datetime


import json

def parse_datatable_args( request, name_mapping=None ):

    params = {}

    sEcho = request.get('sEcho', '1')
    params['echo'] = sEcho

    iDisplayStart  = int(request.get('iDisplayStart', '0'))
    iDisplayLength = int(request.get('iDisplayLength', '10'))
    params['range'] = [iDisplayStart, iDisplayStart+iDisplayLength]

    sSearch = request.get('sSearch', '')
    params['global_filter'] = sSearch

    fields = []
    filters = {}
    # get filters info
    iColumns = int(request.get('iColumns', '0'))
    for i in xrange(iColumns):
        if name_mapping:
            fname = name_mapping[request.get('mDataProp_%s' % i, '')]
        else:
            fname = request.get('mDataProp_%s' % i, '')
        fields.append( fname )
        if request.get('bSearchable_%s' % i, 'false') == 'true':
            p = request.get('sSearch_%s' % i, '')
            if p != '':
                filters[ fname ] = p

    orders = []
    # get sorting info
    iSortingCols = int(request.get('iSortingCols', '0'))
    for i in xrange(iSortingCols):
        j = int(request.get('iSortCol_%s' % i, ''))
        fname = fields[ j ]
        if request.get('bSortable_%s' % j, 'false') == 'true':
            p = request.get('sSortDir_%s' % i, '')
            if p != '':
                orders.append( [fname, p] )

    params['fields'] = fields
    params['filters'] = filters
    params['orders'] = orders

    return params



def parse_orders(orders, names):
    res = []
    for fname, d  in orders:
        if d == 'asc':
            res.append( names[fname] )
        else:
            res.append( '-'+names[fname] )
    return res

def parse_filters(filters, names, global_filter=''):
    if global_filter == '' and filters == {}:
        return None
    if global_filter != '':
        res = {}
        for fname, val in filters.items():
            res[names[fname]+'__contains'] = val
        q = 0
        for name in names.values():
            if q:
                q = q | Q ( **{name+'__contains' : global_filter} )
            else:
                q = Q ( **{name+'__contains' : global_filter} )
        if q:
            if res != {}:
                return Q(**res) & q
            else:
                return q
        else:
            if res != {}:
                return Q(**res)
            else:
                return None
    else:
        res = {}
        for fname, val in filters.items():
            res[names[fname]+'__contains'] = val
        if res != {}:
            return Q(**res)
        else:
            return None

def make_datatable_response_params(echo, total, display, rows, fields, names=None):

    dtask = []
    if names:
        for t in rows:
            d={}
            for n in fields:
                d[names[n]]= t[n]
            dtask.append(d)
    else:
        for t in rows:
            d=[]
            for n in fields:
                d.append(t[n])
            dtask.append(d)

    return { "sEcho": echo, "iTotalRecords": total, "iTotalDisplayRecords": display,
                    "aaData": dtask }


def datatable_entry(request, table_meta, template='core/_datatable.html', parent_template='core/_index.html'):
    tmpl = get_template(template)
    table_meta['parent_template'] = parent_template
    c = Context( table_meta )
    return HttpResponse(tmpl.render(c,))


def datatable_data_answer(request, table_meta, model, db=None):
    row_type = table_meta.get('row_type', 'array')
    if row_type == 'array':
        params = parse_datatable_args(request.GET, dict( (str(i),table_meta['fields'][i]['tname']) for i in xrange(len(table_meta['fields'])) ) )
    elif row_type == 'object':
        params = parse_datatable_args(request.GET)

    print '\nparams = ',params,'\n'

    searchable_names = dict( (f['tname'], f['aname']) for f in filter( lambda u: not u.has_key('searchable') or ( u.has_key('searchable') and u['searchable'] == 'true'), table_meta['fields'] )  )
    names = dict( (f['tname'], f['aname']) for f in table_meta['fields'] )

    filters = parse_filters(params['filters'], searchable_names , params['global_filter'])
    orders = parse_orders(params['orders'], names )

##    total_records = 1000
##    display_records = 1000

    if db:
        objs = model.objects.using(db)
    else:
        objs = model.objects

    total_records = objs.count()

    if filters:
        display_records = objs.filter(filters).count()
    else:
        display_records = total_records


    print '\nfilters = ',filters,'\n'
    print '\norders = ',orders,'\n'

    field_list = [ names[f] for f in params['fields'] ]

    print '\nfields_list = ',field_list,'\n'
    print 'row type =', row_type

    if filters:
        objs = objs.values( *field_list ).filter(filters).order_by(*orders)
    else:
        objs = objs.values( *field_list ).order_by(*orders)

    if params.has_key('range'):
        start,end = params['range']
        if start < 0:
            start = 0
        if end > total_records:
            end = total_records
        objs = objs[ start:end ]

    print '\nQUERY = "',objs.query,'"\n'


    if row_type == 'array':
        resp = make_datatable_response_params( params['echo'], total_records, display_records, objs, field_list)
    else:
        names =  dict( (f['aname'], f['tname']) for f in table_meta['fields'] )
        resp = make_datatable_response_params( params['echo'], total_records, display_records, objs, field_list, names )

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else str(obj)

    return  HttpResponse(json.dumps(resp, ensure_ascii=False, default=dthandler), mimetype='application/json')

  #  return  HttpResponse(" objs =  %s" % objs)






