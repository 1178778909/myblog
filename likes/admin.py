from django.contrib import admin
from .models import LikeRecord, LikeCount

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'content_object', 'user', 'like_time')
