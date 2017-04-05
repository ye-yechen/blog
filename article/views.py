# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
import models
import markdown
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from forms import RegisterForm
from django.http import HttpResponseRedirect
from models import User


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

    for article in articles:
        article.tags = article.tags.split()
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
    article.read_count += 1  # 阅读次数+1
    article.save()
    article.tags = article.tags.split()
    return render(request, 'article_detail.html', {'article': article})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = "/blog"  # 注册成功后跳转到首页

    def form_valid(self, form):
        form.save()
        # name = form.cleaned_data.get('username')
        # psw = form.cleaned_data.get('password')
        # user = authenticate(name=name, psw=psw)
        # login(self.request, user)
        return super(RegisterView, self).form_valid(form)











