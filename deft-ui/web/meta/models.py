from django.db import models
import os


class MetaTask(models.Model):
    meta_id		= models.DecimalField(decimal_places=0, max_digits=12, db_column='META_ID', primary_key=True)
    meta_template	= models.DecimalField(decimal_places=0, max_digits=12, db_column='META_TEMPLATE')
    meta_state          = models.CharField(max_length=16,  db_column='META_STATE', blank=True)
    meta_comment        = models.CharField(max_length=128, db_column='META_COMMENT', blank=True)
    meta_name        	= models.CharField(max_length=128, db_column='META_NAME', blank=True)
    meta_requestor	= models.CharField(max_length=128, db_column='META_REQUESTOR', blank=True)
    meta_manager        = models.CharField(max_length=128, db_column='META_MANAGER', blank=True)
    meta_cloud          = models.CharField(max_length=10,  db_column='META_CLOUD', blank=True)
    meta_site          	= models.CharField(max_length=10,  db_column='META_SITE', blank=True)
    meta_vo		= models.CharField(max_length=16,  db_column='META_VO', blank=True)
    meta_req_ts		= models.DateTimeField()
    meta_upd_ts		= models.DateTimeField()
    class Meta:
        db_table = u'DEFT_META'
        

# Constituent Task
class Task(models.Model):
    task_id		= models.DecimalField(decimal_places=0, max_digits=12, db_column='TASK_ID', primary_key=True)
    task_meta		= models.DecimalField(decimal_places=0, max_digits=12, db_column='TASK_META')
    task_state          = models.CharField(max_length=16,  db_column='TASK_STATE', blank=True)
    task_param          = models.CharField(max_length=4000,db_column='TASK_PARAM', blank=True)
    task_tag            = models.CharField(max_length=16,  db_column='TASK_TAG', blank=True)
    task_comment        = models.CharField(max_length=128, db_column='TASK_COMMENT', blank=True)
    task_vo		= models.CharField(max_length=16,  db_column='TASK_VO', blank=True)
    task_transpath	= models.CharField(max_length=128, db_column='TASK_TRANSPATH', blank=True)
    class Meta:
        db_table = u'DEFT_TASK'
        
class Dataset(models.Model):
    dataset_id		= models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASET_ID', primary_key=True)
    dataset_name 	= models.CharField(max_length=128,  db_column='DATASET_NAME')
    dataset_source 	= models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASET_SOURCE')
    dataset_target	= models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASET_TARGET')
    dataset_meta	= models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASET_META')
    dataset_state	= models.CharField(max_length=16,  db_column='DATASET_STATE')
    dataset_flavor	= models.CharField(max_length=16,  db_column='DATASET_FLAVOR')
    dataset_format	= models.CharField(max_length=16,  db_column='DATASET_FORMAT')
    dataset_comment	= models.CharField(max_length=128,  db_column='DATASET_COMMENT')
    class Meta:
        db_table = u'DEFT_DATASET'

class ProdsysComm(models.Model):
    comm_task		= models.DecimalField(decimal_places=0, max_digits=12, db_column='COMM_TASK', primary_key=True)
    comm_meta		= models.DecimalField(decimal_places=0, max_digits=12, db_column='COMM_META')
    comm_owner		= models.CharField(max_length=16,  db_column='COMM_OWNER')
    comm_cmd		= models.CharField(max_length=256,  db_column='COMM_CMD')
    comm_ts		= models.DecimalField(decimal_places=0, max_digits=12, db_column='COMM_TS')
    comm_comment	= models.CharField(max_length=128,  db_column='COMM_COMMENT')
    class Meta:
        db_table = u'PRODSYS_COMM'

