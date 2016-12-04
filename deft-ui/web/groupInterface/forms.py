from django.db import models
from django.forms import ModelForm
from groupInterface.models import *
from deft.dbaccess import localdb
import os


# If you want to use the extended Alden version, set the env variable LOCALDB to anything. If not, clear it.

class MetaForm(ModelForm):
    class Meta:
        exclude = ['slug',]
        model = MetaTask

class TaskForm(ModelForm):
    class Meta:
        exclude = ['slug',]
        model = Task

class DeftUserForm(ModelForm):
    class Meta:
        model = DeftUser
        exclude = ['slug',]

class DeftGroupForm(ModelForm):
    class Meta:
        model = DeftGroup
        exclude = ['slug',]

## class MetaForm(ModelForm):
##     class Meta:
##         model = MetaTask

## class MetaForm(ModelForm):
##     class Meta:
##         model = MetaTask

## class MetaForm(ModelForm):
##     class Meta:
##         model = MetaTask

## class MetaForm(ModelForm):
##     class Meta:
##         model = MetaTask

## class MetaForm(ModelForm):
##     class Meta:
##         model = MetaTask

## class MetaForm(ModelForm):
##     class Meta:
##         model = MetaTask

## class MetaForm(ModelForm):
##     class Meta:
##         model = MetaTask

