from django.contrib import admin
from .models import Folder, File

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'parent']

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'owner', 'parent', 'date_time']