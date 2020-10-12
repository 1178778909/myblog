import threading

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

class Send_Mail(threading.Thread):
    def __init__(self, subject, text, email):
        self.subject = subject
        self.text = text
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
            html_message=self.text
        )

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    root = models.ForeignKey('self', null=True, related_name="root_comment", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, related_name="parent_comment", on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, null=True, related_name="replies", on_delete=models.CASCADE)

    def send_mail(self):
        # 发送邮件通知
        if self.parent is None:
            # 评论我的博客
            subject = '博客回复通知'
            email = self.content_object.get_email()
        else:
            # 回复博客评论
            subject = '评论回复通知'            
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render(None, 'comment/send_email.html', context).content.decode('utf-8')
            send_mail = Send_Mail(subject, text, email)
            send_mail.start()


    def __str__(self):
        return self.text

    class Meta:
        # 按时间正序排列
        ordering = ['comment_time']
