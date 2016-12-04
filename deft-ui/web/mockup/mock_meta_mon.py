#!/usr/bin/python
import django
from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse


t = get_template('deft_test_meta.html')

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

html = t.render(Context({'my_name': 'mxp', 'title' : 'DEFT Meta-Task Monitor', 'metas': metas}))

print html
