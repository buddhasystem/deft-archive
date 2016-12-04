# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.db import models
from django.forms import ModelForm

from django.shortcuts import render, render_to_response
from django.template import Context, Template, RequestContext
from django.template.loader import get_template

from groupInterface.models import *
from groupInterface.forms import *
from serializers import *

### Boilerplate for the DEFT UI Meta-Task and Task server pages
###

def index(request):
    return HttpResponse("This is the task main page.")

def home(request):
    c=Context()
    return HttpResponse(content='Placeholder for the DEFT Main Page. Starting point for navigation across Task and Meta-Task monitoring, and editing/authorization screens ', mimetype='text/html')



def metaCreate(request):
    if request.method == "POST":
        meta_form = MetaForm(request.POST)

        if meta_form.is_valid():
            success = True
            meta_task = meta_form.save()
            post_context = {'success':success, 'meta_form':meta_form}
            return render_to_response('groupInterface/meta_task_creation.html', post_context, context_instance=RequestContext(request))
        else:
            failure = True
            post_context = {'failure':failure, 'meta_form':meta_form}
            return render_to_response('groupInterface/meta_task_creation.html', post_context, context_instance=RequestContext(request))

    else:
        meta_form = MetaForm()
    pre_context = {'meta_form':meta_form}
    return render_to_response('groupInterface/meta_task_creation.html', pre_context, context_instance=RequestContext(request))


def taskCreate(request):
    if request.method == "POST":
        task_form = TaskForm(request.POST)

        if task_form.is_valid():
            success = True
            task = task_form.save()
            post_context = {'success':success, 'task_form':task_form}
            return render_to_response('groupInterface/task_creation.html', post_context, context_instance=RequestContext(request))
        else:
            failure = True
            post_context = {'failure':failure, 'task_form':task_form}
            return render_to_response('groupInterface/task_creation.html', post_context, context_instance=RequestContext(request))

    else:
        task_form = TaskForm()
        pre_context = {'task_form':task_form}
        return render_to_response('groupInterface/task_creation.html', pre_context, context_instance=RequestContext(request))

# Dataset sources have been AFS, attached files, direct listing. Deduplication is important.
# Task creation needs to be able to draw from validated datasets
# - Dataset validation needs to check for duplicate runs
# - Dataset validation needs to check for available files (no empty dataset)
# - Container creation?
# - Datasets sortable by metadata and not just by dataset number?

# Task creation needs to be able to see what was in the metatask
# The metatask creation needs to be able to build in the DAG, or to be able to absorb and process the XML spec
# The task needs to configure the output automatically based on the tag
# Parse tag and understand it so that the other fields are filled with reasonable defaults
# Metatask is going to carry most of the info, not the task! Move the majority of the model fields over from task to meta
# Handle tag creation and population in the database
# Handle extension of an existing task with new datasets -- one-click, perhaps even doing so for a range of tasks.

# We need a task and metatask management view
# - Export that view in CSV as well for ease of hand-manipulation and accounting in code# - Multicolumn, editable
# - Fluid, sortable, draggable for column reordering
# - Bulk update ability (dragging a value or mass pasting
# - Interface for changing all of a selection
# - Bulk approval ability
# - Approve all based on criteria
# - Filter by regular expression
# Task status management view -- ability to change status and stop tasks in ranges by username, task number range and tag, metatask
# - Needs to be able to clean up the whole chain as well -- refer to the metatask

# Bulk DaTrI request interface based on dataset interface... ask Mikhail abou that.

# Each task request (not meta -- ??) needs a comments thread associated. That thread needs to be persistent for a while, then possibly go away... and needs to have usernames attached with no ambiguity. I assume this is easier in django than otherwise.

# Need a spreadsheet population system (CSV, XML?)

# This is the group request system, and will be at least initially independent from the MC request system.

# Allow output of the standard files for submission as it stands with prodsys2
# Allow inspection of the files before export


# Merge interface -- no real understanding yet of that process


