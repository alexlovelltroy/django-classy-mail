from django.contrib import admin
from .models import EmailTemplate

class TemplatedEmailMessageAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'subject_content')
    list_editable = ('subject_content', )
    ordering = ('name',)

admin.site.register(EmailTemplate, TemplatedEmailMessageAdmin)
