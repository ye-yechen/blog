# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
import models
import markdown
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from forms import RegisterForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings as django_settings
from token import token_confirm


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
        user=request.user,
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
        return super(RegisterView, self).form_valid(form)


def active_user(request, token):    # 认证激活函数
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
            return render(request, 'message.html',
                          {'message': u'对不起，验证链接已经过期，请重新<a href=\"' + unicode(django_settings.DOMAIN) + u'/signup\">注册</a>'})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'message.html', {'message': u"对不起，您所验证的用户不存在，请重新注册"})
    user.is_active = True
    user.save()
    message = u'验证成功，请进行<a href=\"' + unicode(django_settings.ROOT_URLCONF) + u'/login\">登录</a>操作'
    return render(request, 'message.html', {'message':message})


def login_page(request):
    redirect_to = request.META.get('HTTP_REFERER', '/')
    return render(request, 'login.html', {'redirect_to': redirect_to})


def login_site(request):    # 登入
    if request.method == 'POST':
        # request.META 是一个Python字典，包含了所有本次HTTP请求的Header信息
        redirect_to = request.POST.get('next')  # 获取隐藏域的值，进行页面跳转
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)  # 使用 Django 的 authenticate 方法来验证
        if user:
            login(request, user)
            return HttpResponseRedirect(redirect_to)
        else:
            return render(request, 'login.html', {
                'login_err': '用户名或者密码不正确'
            })


def logout_site(request):
    logout(request)
    redirect_to = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(redirect_to)





