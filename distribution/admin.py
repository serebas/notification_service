from django.contrib import admin
from .models import *

class DistributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp_start', 'timestamp_end', 'filter', 'message_text')
    list_display_links = ('id',)
    search_fields = ('filter',)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'MNC', 'TAG', 'timezone')
    list_display_links = ('id',)
    search_fields = ('phone_number', 'MNC', 'TAG', 'timezone')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp_create', 'status', 'distribution', 'client')
    list_display_links = ('id',)
    search_fields = ('timestamp_create', 'status', 'distribution', 'client')

admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MessageAdmin)