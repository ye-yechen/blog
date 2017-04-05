# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    psw = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    notes = models.TextField()  # 备注
    image = models.CharField(max_length=100, blank=True)  # 图像地址
    gender = models.BooleanField(default=False)  # 性别：0->男
    status = models.BooleanField(default=0)  # 账号是否激活
    validate_code = models.CharField(max_length=50, blank=True)  # 激活码
    register_time = models.DateTimeField()

    def __unicode__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    content_md = models.TextField()  # markdown格式的内容
    content_html = models.TextField()  # html格式的内容
    read_count = models.IntegerField(default=0)  # 阅读次数
    summary = models.CharField(max_length=300)  # 摘要
    tags = models.CharField(max_length=30, blank=True)  # 标签
    create_time = models.DateTimeField()  # 只在第一次创建model时更新时间
    update_time = models.DateTimeField()  # 每次修改model时更新时间
    deleted = models.BooleanField(default=False)  # 文章是否被删除
    allow_comment = models.BooleanField(default=False)  # 文章是否允许评论
    category = models.CharField(max_length=30,blank=True)

    def __unicode__(self):
        return self.title




