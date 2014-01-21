from django.contrib import admin
from .models import EmailTemplate, EmailMessageLog

class TemplatedEmailMessageAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'subject_content')
    list_editable = ('subject_content', )
    ordering = ('name',)

class MessageLogAdmin(admin.ModelAdmin):
    search_fields = ['to_header', 'subject']
    list_display = ('to_header', 'subject', 'sent')
    ordering = ('-sent',)

admin.site.register(EmailTemplate, TemplatedEmailMessageAdmin)
admin.site.register(EmailMessageLog, MessageLogAdmin)
