# -*- coding:utf-8 -*-
from django.shortcuts import render
import models
import markdown
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request, page=1):
    articles = models.Article.objects.all().order_by('-create_time')
    # 分页
    paginator = Paginator(articles, 15)  # 每页15项
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'articles': articles})


def publish(request):
    return render(request, 'publish.html')


def save_article(request):  # 保存文章
    title = request.POST.get('title')
    content_md = request.POST.get('content')
    tags = request.POST.get('tags')
    content_html = markdown.markdown(content_md)
    now = datetime.datetime.now()
    create_time = now
    update_time = now
    summary = content_md[:50]
    models.Article.objects.create(
        title=title,
        content_md=content_md,
        content_html=content_html,
        tags=tags,
        summary=summary,
        create_time=create_time,
        update_time=update_time,
    )
    articles = models.Article.objects.all().order_by('-create_time')
    return render(request, 'index.html', {'articles': articles})


def article_detail(request, article_id):  # 全文阅读
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'article_detail.html', {'article': article})

