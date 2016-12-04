from django.db import models
from django.forms import ModelForm
from jedi.models import *
import os

#base_path=os.environ['HOME']

class JEDITaskForm(ModelForm):
    class Meta:
        model = JEDITask


class JEDIDatasetForm(ModelForm):
    class Meta:
        model = JEDIDataset



class JEDIDatasetContentForm(ModelForm):
    class Meta:
        model = JEDIDatasetContent


