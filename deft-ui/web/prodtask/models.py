from django.db import models

# Create your models here.

class ProdTask(models.Model):
    reqid = models.BigIntegerField(primary_key=True, db_column='REQID') # Field name made lowercase.

    swrelease = models.CharField(max_length=20, db_column='SWRELEASE')
    lparams = models.CharField(max_length=22, db_column='LPARAMS')
    ppstate = models.CharField(max_length=12, db_column='PPSTATE')

    priority = models.IntegerField(db_column='priority')

    parent_id = models.IntegerField(null=True, db_column='PARENT_TID', blank=True)
    bug_report = models.IntegerField(null=True, db_column='BUG_REPORT', blank=True)
    cpu_per_event = models.IntegerField(null=True, db_column='CPUPEREVENT', blank=True)
    first_inputfile_n = models.IntegerField(null=True, db_column='FIRST_INPUTFILE_N', blank=True)
    phys_group = models.CharField(max_length=22, db_column='PHYS_GROUP')
    ctag = models.CharField(max_length=12, db_column='CTAG')
    bug_reference = models.IntegerField(null=True, db_column='BUG_REFERENCE', blank=True)

    BUG_REFERENCE = models.IntegerField(null=True,db_column="BUG_REFERENCE",max_length=22)

    LASTMODIFIED  = models.DateTimeField(db_column="LASTMODIFIED",max_length=7)
    DSN = models.CharField( db_column="DSN",max_length=15)
    PRODSTEP= models.CharField(db_column="PRODSTEP",max_length=40)
    TRF= models.CharField(db_column="TRF",max_length=80)
    TRFV=models.CharField(db_column="TRFV",max_length=40)
    email=models.CharField(db_column="email",max_length=60)
    memory= models.IntegerField(null=True,db_column="memory",max_length=22)
    CONFIGURATION_TAG= models.CharField(db_column="CONFIGURATION_TAG",max_length=30)
    TOTAL_AVAIL_JOBS=  models.IntegerField(db_column="TOTAL_AVAIL_JOBS",max_length=22)
    TIDTYPE = models.CharField(null=True,db_column="TIDTYPE",max_length=12)
    INPUTDATASET = models.CharField(db_column="INPUTDATASET",max_length=150)
    taskname= models.CharField(db_column="taskname",max_length=130)
    VPARAMS= models.CharField(db_column="VPARAMS",max_length=4000)
    TOTAL_F_EVENTS= models.IntegerField(null=True, db_column="TOTAL_F_EVENTS",max_length=22)
    FORMATS=  models.CharField(db_column="FORMATS",max_length=256)
    TOTAL_REQ_JOBS= models.IntegerField(null=True,  db_column="TOTAL_REQ_JOBS",max_length=22)
    TOTAL_DONE_JOBS= models.IntegerField(null=True, db_column="TOTAL_DONE_JOBS",max_length=22)
    POSTPRODUCTION=  models.CharField( db_column="POSTPRODUCTION",max_length=128)
    TOTAL_INPUT_FILES = models.IntegerField(null=True,  db_column="TOTAL_INPUT_FILES",max_length=22)
    TRF_CACHE = models.IntegerField(null=True, db_column= "EVENTS_PER_FILE",max_length=22)
    TRF_CACHE=  models.CharField(db_column="TRF_CACHE",max_length=30)
    status =  models.CharField(db_column="status",max_length=12)
    PHYS_REF = models.CharField(db_column="PHYS_REF",max_length=65)
    PRODTAG =  models.CharField( db_column="PRODTAG",max_length=50)

    start_time = models.IntegerField(null=True, db_column="startTime", max_length=22)

    class Meta:
        db_table = u't_task_request'


