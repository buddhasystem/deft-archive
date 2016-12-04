#!/usr/bin/python
import django
from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse

t = get_template('deft_test_lib.html')

templates = []

info = [
	{
	'tmpl_id':'187',
	'tmpl_name':'mc13.8TeV.Pythia.Ztautau332',
	'tmpl_author':'W.Ehrenfeld',
	'tmpl_pwg':'Z',
	'tmpl_created_ts':'2013-07-01 12:07'
	},
	{
	'tmpl_id':'203',
	'tmpl_name':'mc13.8TeV.Herwig.Ztautau200',
	'tmpl_author':'W.Ehrenfeld',
	'tmpl_pwg':'Z',
	'tmpl_created_ts':'2013-07-03 13:11'
	},
	{
	'tmpl_id':'011',
	'tmpl_name':'Nightly.SL6.beta',
	'tmpl_author':'A.Undrus',
	'tmpl_pwg':'S',
	'tmpl_created_ts':'2013-07-22 10:10'
	},
	{
	'tmpl_id':'018',
	'tmpl_name':'LBNE.beamsim',
	'tmpl_author':'K.Yarritu',
	'tmpl_pwg':'N',
	'tmpl_created_ts':'2013-07-28 11:16'
	}
	]

for d in info:
	templates.append(d)


html = t.render(Context({'my_name': 'mxp', 'title' : 'DEFT Template LIbrary', 'templates': templates}))

print html
