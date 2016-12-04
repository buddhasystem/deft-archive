from django.db import models
import os

# JEDITask
class JEDITask(models.Model):
    jeditaskid		= models.DecimalField(decimal_places=0, max_digits=12, db_column='JEDITASKID', primary_key=True)
    taskname        = models.CharField(max_length=128,  db_column='TASKNAME', blank=True)
    status          = models.CharField(max_length=64, db_column='STATUS', blank=True)
    username        = models.CharField(max_length=128, db_column='USERNAME', blank=True)
    vo	            = models.CharField(max_length=16,  db_column='VO', blank=True)
    creationdate	= models.DateTimeField(db_column='CREATIONDATE')
    modificationtime		= models.DateTimeField(db_column='MODIFICATIONTIME')

    class Meta:
        db_table = u'JEDI_TASKS'

# JEDIDataset
class JEDIDataset(models.Model):

    jeditask		= models.ForeignKey(JEDITask, db_column='JEDITASKID')
    datasetid		= models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASETID', primary_key=True)
    datasetname     = models.CharField(max_length=128,  db_column='DATASETNAME', blank=True)
    status          = models.CharField(max_length=64, db_column='STATUS', blank=True)
    site            = models.CharField(max_length=128, db_column='SITE', blank=True)
    nevents            = models.CharField(max_length=128, db_column='NEVENTS', blank=True)

    vo	            = models.CharField(max_length=16,  db_column='VO', blank=True)
    creationdate	= models.DateTimeField(db_column='CREATIONTIME')
    modificationtime		= models.DateTimeField(db_column='MODIFICATIONTIME')

    class Meta:
        db_table = u'JEDI_DATASETS'

# JEDIDatasetContent
class JEDIDatasetContent(models.Model):

    dataset		   = models.ForeignKey(JEDIDataset, db_column='DATASETID')

    fileid          = models.CharField(max_length=128,  db_column='FILEID', blank=True, primary_key=True)

    status          = models.CharField(max_length=64, db_column='STATUS', blank=True)

    fsize           = models.CharField(max_length=128, db_column='FSIZE', blank=True)

    lfn             = models.CharField(max_length=128, db_column='LFN', blank=True)
    guid	        = models.CharField(max_length=16,  db_column='GUID', blank=True)

    creationdate	= models.DateTimeField(db_column='CREATIONDATE')
    lastattempttime		= models.DateTimeField(db_column='LASTATTEMPTTIME')

    class Meta:
        db_table = u'JEDI_DATASET_CONTENTS'


