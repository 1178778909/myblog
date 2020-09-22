from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING)

    root = models.ForeignKey('self', null=True, related_name="root_comment", on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', null=True, related_name="parent_comment", on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, null=True, related_name="replies", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text

    class Meta:
        # 按时间正序排列
        ordering = ['comment_time']
