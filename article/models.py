# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class User(models.Model):
#     name = models.CharField(max_length=50)
#     psw = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     notes = models.TextField()  # 备注
#     image = models.CharField(max_length=100, blank=True)  # 图像地址
#     gender = models.BooleanField(default=False)  # 性别：0->男
#     status = models.BooleanField(default=0)  # 账号是否激活
#     validate_code = models.CharField(max_length=50, blank=True)  # 激活码
#     register_time = models.DateTimeField()
#
#     def __unicode__(self):
#         return self.name


class Tag(models.Model):    # 标签类
    tag_name = models.CharField(max_length=20)
    create_time = models.DateTimeField()
    tag_desc = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.tag_name


class Category(models.Model):   # 文章分类
    category_name = models.CharField(max_length=20)
    create_time = models.DateTimeField()
    category_desc = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.category_name


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    content_md = models.TextField()  # markdown格式的内容
    content_html = models.TextField()  # html格式的内容
    read_count = models.IntegerField(default=0)  # 阅读次数
    summary = models.CharField(max_length=300)  # 摘要
    tags = models.CharField(max_length=30, blank=True)  # 标签(过时的)
    tags_2 = models.ManyToManyField(Tag, verbose_name='tags', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # 分类
    create_time = models.DateTimeField()  # 只在第一次创建model时更新时间
    update_time = models.DateTimeField()  # 每次修改model时更新时间
    deleted = models.BooleanField(default=False)  # 文章是否被删除
    allow_comment = models.BooleanField(default=False)  # 文章是否允许评论
    # category = models.CharField(max_length=30,blank=True)
    comment_nums = models.IntegerField(default=0)  # 此博客的评论条数

    def __unicode__(self):
        return self.title


class Reply(models.Model):  # 博客的回复
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # 评论者
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    reply_time = models.DateTimeField()
    is_comment = models.BooleanField(default=True)  # 区分是评论还是对评论的回复

    def __unicode__(self):
        return self.content


class Message(models.Model):    # 留言
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # 留言者
    content = models.TextField()
    message_time = models.DateTimeField()

    def __unicode__(self):
        return self.content


class Photo(models.Model):  # 照片
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='upload/', blank=True, null=True)
    photo_name = models.CharField(max_length=50)
    photo_path = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    def __unicode__(self):
        return self.photo_name
