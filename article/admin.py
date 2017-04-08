from django.contrib import admin
from article.models import Article, Reply, Category, Tag
# from article.models import User
# Register your models here.

admin.site.register(Article)
# admin.site.register(User)
admin.site.register(Reply)
admin.site.register(Tag)
admin.site.register(Category)