from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','title', 'description', 'complete', 'created_at')
    search_fields = ('title', 'user')
    list_filter = ('complete', 'created_at',)

admin.site.register(Task, TaskAdmin)