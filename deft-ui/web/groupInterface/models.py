from django.db import models
from django.forms import ModelForm
from django.core import validators
from deft.dbaccess import localdb
import os

# Add a model for tags (sync with AMI? Direct Draw? Population cron?) -- associate user that created
# Add a model for datasets (sync with AMI/prodsys? Direct Draw? Population cron?)
# Leave in the necessary fields for backward compatibility



# Meta-Task
class MetaTask(models.Model):
    meta_id	= models.DecimalField(decimal_places=0, max_digits=12, db_column='META_ID', primary_key=True)
    meta_state = models.CharField(max_length=16,  db_column='META_STATE', blank=True) # Ripe for a type
    meta_comment = models.CharField(max_length=128, db_column='META_COMMENT', blank=True)
    meta_requestor = models.CharField(max_length=128, db_column='META_REQUESTOR', blank=True)
    # Add meta_owner?
    meta_manager = models.CharField(max_length=128, db_column='META_MANAGER', blank=True)
    meta_vo = models.CharField(max_length=16, db_column='META_VO', blank=True)
    meta_req_ts	= models.DateTimeField()
    meta_upd_ts	= models.DateTimeField()
    # Potential fields:

    # Output Formats: NTUP_EGAMMA,NTUP_TAU (Selector? ForeignKey?)
    # Transformation Type (Select list): Reco_trf.py
    # Transformation Version (ForeignKey): 17.2.7.5.20
    # Transformation Cache: AtlasPhysics...
    # Config Tag (ForeignKey) (already in Task, to be removed)
    # First file number in input dataset(??): 1
    # DBRelease: latest (or 5.1.1)
    # asetup: none
    # autoConfiguration: everything
    # beamType: none
    # conditionsTag: None
    # extraParameter (??): none
    # geometryVersion: None (ATLAS_CSC_02_00_00)
    # postExec: (long string)
    # postInclude: None (long string)
    # preExec: (long string)
    # preInclude: None (long string)
    # tmpAOD (??): None
    # tmpESD (??): None
    # topOptions (??): None
    # triggerConfig: None
    # Provenance (ATLAS, Group, Extended)
    # Project Operation mode: (Catchall string for modifications)
    # Comment/Physics Long: group_MERGE_list
    # Group (from task): bphysics (selector/ForeignKey)
    # 
    
    def __unicode__(self):
        return str(self.meta_id)

    class Meta:
        db_table = u'DEFT_META'


class Task(models.Model):
    # To add (??):

    # CPU per event: 10
    # Memory Usage: 3500
    # SW Release (ForeignKey): 17.2.7 (Pull from AGIS on cron?)
    # Total Generated Events: 1 (Going away?)
    # Total Input Files (??): 1
    # Associated blog/comment thread entry
    
    ALLOWED_FORMATS=[('NTUP_TOP','Top-Group Ntuple (NTUP_TOP)'),
                     ('OTHER','Other Format'),
                     ] # Preliminary - Fill this out (ARS) (Perhaps new class?)
    STATES=[('p','Paused'),
            ('r','Running'),
            ('d','Finished'),
            ('f','Failed'),
            ] # Preliminary - Fill this out (ARS) (Perhaps new class?)
    VOS=[('zp','ATLAS'),
         ('zh','CMS'),
         ] # Preliminary - Fill this out (ARS) (Perhaps new class?)


    task_id	= models.DecimalField(decimal_places=0, max_digits=12, db_column='TASK_ID', primary_key=True)
    task_meta = models.ForeignKey('MetaTask') # See the MetaTask class. OneToOneField indicates table inheritance. https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types

    task_comment = models.CharField(max_length=128, db_column='TASK_COMMENT', blank=True)
    task_dataset = models.ForeignKey('Dataset') #:group.perf-tau.periodM.DESD_ZMUMU.pro09.embedding-02-39.Ztautaull_isol_mfsim_rereco_p851_EXT0 #Changed from ds
    task_destination = models.ForeignKey('StorageElement') #UKI-LT2-QMUL_PHYS-TOP,NET2_PHYS-TOP
    task_diskcount = models.PositiveSmallIntegerField(db_column='TASK_DISKCOUNT')
    task_events_per_job = models.PositiveIntegerField(db_column='TASK_EVENTS_PER_JOB') # :1000
    task_formats = models.CharField(max_length=80, default=ALLOWED_FORMATS[0][1], db_column='TASK_FORMATS') #:NTUP_TOP (Ripe for another table instead of a definition)
    task_group = models.ForeignKey('DeftGroup') #:GR_TOP (Move to meta!)
    # Task Subgroup?
    task_num_events = models.PositiveSmallIntegerField(db_column='TASK_NUM_EVENTS') #:all
    task_owner = models.ForeignKey('DeftUser') #:minoru.hirose@cern.ch
    task_param = models.CharField(max_length=4000,db_column='TASK_PARAM', blank=True)
    task_priority = models.PositiveSmallIntegerField(db_column='TASK_PRIORITY') #:750
    task_project = models.ForeignKey('Project') #:data11_7TeV
    task_project_mode = models.CharField(max_length=300, db_column='TASK_PROJECT_MODE')# :spacetoken=ATLASDATADISK;
    task_ram = models.PositiveSmallIntegerField(db_column='TASK_RAM') #:3500
    task_state = models.CharField(max_length=16,  db_column='TASK_STATE')
    task_tag = models.CharField(max_length=20,  db_column='TASK_TAG', blank=True)# :p937
    task_total_num_genev = models.IntegerField(db_column='TASK_TOTAL_GENEVENTS')# :-1
    task_transpath = models.CharField(max_length=128, db_column='TASK_TRANSPATH', blank=True)
    task_vo	= models.CharField(max_length=16,  db_column='TASK_VO', blank=True)
    task_lumiblock = models.BooleanField(db_column='TASK_LUMIBLOCK')#; yes
    task_reprocessing = models.BooleanField(db_column='TASK_REPROCESSING')#; yes

    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return str(self.task_id)
    class Meta:
        db_table = u'DEFT_TASK'

class DeftUser(models.Model):
    user_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='TASK_ID', primary_key=True)
    user_name = models.CharField(max_length=128, db_column='USER_NAME')
    user_dn = models.CharField(max_length=100, db_column='USER_DN')
    user_email = models.EmailField(max_length=274, db_column='USER_EMAIL')
    user_group = models.ForeignKey('DeftGroup')
    user_project = models.ForeignKey('Project')
    user_vo = models.ForeignKey('VO')
    user_tags = models.CharField(max_length=20,  db_column='USER_TAG', blank=True)
    user_location = models.ForeignKey('Location')
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return self.user_name
    class Meta:
        db_table = u'DEFT_USERS'

class DeftGroup(models.Model):
    group_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='GROUP_ID', primary_key=True)
    group_name = models.CharField(max_length=128, db_column='GROUP_NAME')
    group_vo = models.ForeignKey('VO')
    group_tags = models.CharField(max_length=20,  db_column='GROUP_TAG', blank=True)
    group_description = models.CharField(max_length=100, db_column='GROUP_DESCRIPTION', blank=True)
    group_contactemail = models.EmailField(max_length=274, db_column='GROUP_CONTACTEMAIL')
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return self.group_name
    class Meta:
        db_table = u'DEFT_GROUPS'



class Project(models.Model):
    proj_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='PROJ_ID', primary_key=True)
    proj_name = models.CharField(max_length=128, db_column='PROJ_NAME')
    proj_vo = models.ForeignKey('VO')
    proj_tags = models.CharField(max_length=20,  db_column='PROJ_TAG', blank=True)
    proj_description = models.CharField(max_length=200, blank=True, db_column='PROJ_DESCRIPTION')
    proj_contactemail = models.EmailField(max_length=274, db_column='PROJ_CONTACTEMAIL')
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return self.proj_name
    class Meta:
        db_table = u'DEFT_PROJECT'

class VO(models.Model):
    vo_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='VO_ID', primary_key=True)
    vo_name = models.CharField(max_length=16, db_column='VO_NAME')
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return self.vo_name
    class Meta:
        db_table = u'DEFT_VO'

class Location(models.Model):
    loc_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='LOC_ID', primary_key=True)
    loc_name = models.CharField(max_length=64, db_column='LOC_NAME')
    loc_country = models.CharField(max_length=64, db_column='LOC_COUNTRY')
    loc_region = models.CharField(max_length=64, db_column='LOC_REGION')
    loc_vo = models.ForeignKey('VO')
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return self.loc_name
    class Meta:
        db_table = u'DEFT_LOCATION'


class StorageElement(models.Model):
    se_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='SE_ID', primary_key=True)
    se_name = models.CharField(max_length=90, db_column='SE_NAME')
    se_location = models.ForeignKey('Location')
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return self.se_name
    class Meta:
        db_table = u'DEFT_SE'

class Dataset(models.Model):
    dataset_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASET_ID', primary_key=True)
    dataset_name = models.CharField(max_length=128,  db_column='DATASET_NAME')
    dataset_source = models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASET_SOURCE')
    dataset_target = models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASET_TARGET')
    dataset_meta = models.DecimalField(decimal_places=0, max_digits=12, db_column='DATASET_META')
    dataset_state = models.CharField(max_length=16,  db_column='DATASET_STATE')
    dataset_flavor = models.CharField(max_length=16,  db_column='DATASET_FLAVOR')
    dataset_format = models.CharField(max_length=16,  db_column='DATASET_FORMAT')
    dataset_comment = models.CharField(max_length=128,  db_column='DATASET_COMMENT')
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return str(self.dataset_id)
    class Meta:
        db_table = u'DEFT_DATASET'

class ProdsysComm(models.Model):
    comm_task = models.DecimalField(decimal_places=0, max_digits=12, db_column='COMM_TASK', primary_key=True)
    comm_meta = models.DecimalField(decimal_places=0, max_digits=12, db_column='COMM_META')
    comm_owner = models.CharField(max_length=16,  db_column='COMM_OWNER')
    comm_cmd = models.CharField(max_length=256,  db_column='COMM_CMD')
    comm_ts = models.DecimalField(decimal_places=0, max_digits=12, db_column='COMM_TS')
    comm_comment = models.CharField(max_length=128,  db_column='COMM_COMMENT')
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return str(self.comm_task)
    class Meta:
        db_table = u'PRODSYS_COMM'
