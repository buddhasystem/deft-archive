import os
from django.contrib import admin

from groupInterface.models import MetaTask
from groupInterface.models import Task
from groupInterface.models import Dataset
from groupInterface.models import ProdsysComm
from groupInterface.models import DeftUser
from groupInterface.models import DeftGroup
from groupInterface.models import Project
from groupInterface.models import VO
from groupInterface.models import Location
from groupInterface.models import StorageElement

admin.site.register(DeftUser)

class DeftUserInline(admin.TabularInline):
    model = DeftUser
    extra = 3

class DeftGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'group_name')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('proj_id', 'proj_name')

class VOAdmin(admin.ModelAdmin):
    list_display = ('vo_id', 'vo_name')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('loc_id', 'loc_name')

class StorageElementAdmin(admin.ModelAdmin):
    list_display = ('se_id', 'se_name')


admin.site.register(DeftGroup, DeftGroupAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(VO, VOAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(StorageElement, StorageElementAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_meta', 'task_state', 'task_comment')
    ## fieldsets = [
    ##     (None,               {'fields': ['question']}),
    ##     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ## ]
    #inlines = [UserInline]
    list_filter = ['task_id']
    search_fields = ['task_id', 'task_meta']
    #date_hierarchy = 'task_id'

class MetaAdmin(admin.ModelAdmin):
    list_display = ('meta_id', 'meta_comment')
    ## fieldsets = [
    ##     (None,               {'fields': ['question']}),
    ##     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ## ]
    #inlines = [UserInline]
    list_filter = ['meta_id']
    search_fields = ['meta_id']
    #date_hierarchy = 'task_id'
    
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('dataset_id', 'dataset_source', 'dataset_target')

admin.site.register(MetaTask, MetaAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Dataset, DatasetAdmin)
