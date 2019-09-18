from django.contrib import admin
from .models import File

# Register your models here.
class FilesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'description', 'type', 'file', 'created_by']}),
    ]
    list_display = ['name', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name']

admin.site.register(File, FilesAdmin)
