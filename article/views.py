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
from collections import defaultdict, OrderedDict


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
    if not request.user.is_authenticated():  # 用户未登录，不能发表文章
        return render(request, 'login.html')
    categories = models.Category.objects.all()  # 查询所有分类
    return render(request, 'publish.html', {'categories': categories})


def save_article(request):  # 保存文章
    if not request.user.is_authenticated():  # 用户未登录，不能发表文章
        return render(request, 'login.html')
    title = request.POST.get('title')
    content_md = request.POST.get('content')
    category_name = request.POST.get('category')
    category = models.Category.objects.get(category_name=category_name)  # 根据名称查找分类
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
        category=category,
        tags=tags,
        summary=summary,
        user=request.user,
        create_time=create_time,
        update_time=update_time,
    )
    articles = models.Article.objects.all().order_by('-create_time')
    for article in articles:
        article.tags = article.tags.split()
    return render(request, 'index.html', {'articles': articles})


def article_detail(request, article_id):  # 全文阅读
    article = models.Article.objects.get(pk=article_id)  # 查找博客
    article.read_count += 1  # 阅读次数+1
    article.save()
    article.tags = article.tags.split()

    replies = models.Reply.objects.filter(article_id=article_id)  # 查找此博客的所有回复
    # for reply in replies:
    #     print reply.author.username
    return render(request, 'article_detail.html', {'article': article, 'replies': replies})


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


def logout_site(request):   # 注销
    logout(request)
    redirect_to = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(redirect_to)


def reply(request, article_id):  # 评论
    if not request.user.is_authenticated():  # 用户未登录，不能发表评论
        return render(request, 'login.html')

    if request.method == 'POST':
        article = models.Article.objects.get(pk=article_id)  # 获取此文章
        reply_time = datetime.datetime.now()
        content_all = request.POST.get('reply_content')
        author = request.user     # 评论者是当前登录的人
        if content_all[0] == '@':   # 表示是回复某个评论(@某个人)
            who = content_all[1:].split()[0]  # 获取评论框中被@的作者名字
            user_len = len(who)+1  # 加上@后的长度
            content = content_all[user_len:]    # 评论内容
            models.Reply.objects.create(
                content=content_all,
                author=author,
                article=article,
                reply_time=reply_time,
                is_comment=False    # 不是评论
            )
        else:   # 表示直接评论文章
            content = request.POST.get('reply_content')
            user = request.user
            models.Reply.objects.create(
                content=content,
                author=author,
                article=article,
                reply_time=reply_time
            )
            article.comment_nums += 1  # 文章评论数+1
            article.save()

        article.tags = article.tags.split()
        replies = models.Reply.objects.filter(article_id=article_id)  # 查找此博客的所有回复
        return render(request, 'article_detail.html', {'article': article, 'replies': replies})


# def archive_tool():  # 文章归档工具方法
#     # 获取到降序排列的精确到月份且已去重的文章发表时间列表
#     date_list = models.Article.objects.datetimes('created_time', 'month', order='DESC')
#     # 并把列表转为一个字典，字典的键为年份，值为该年份下对应的月份列表
#     date_dict = defaultdict(date_list)
#     for d in date_list:
#         date_dict[d.year].append(d.month)   # [(2017,[04,02,01]),(2016,[12,10,06,01]),...]
#     # 模板不支持defaultdict，因此我们把它转换成一个二级列表，由于字典转换后无序，因此重新降序排序
#     return sorted(date_dict.items(), reverse=True)


def archive(request):   # 文章归档
    date_list = models.Article.objects.datetimes('create_time', 'month', order='DESC')
    article_dict = OrderedDict()
    for date in date_list:
        year = int(date.year)
        month = int(date.month)
        article_list = models.Article.objects.filter(create_time__year=year, create_time__month=month)
        # article_dict.setdefault(date, []).append(article_list)
        article_dict[date] = article_list
    return render(request, 'archive.html', {'data_list': date_list, 'article_dict': article_dict})


def search_archive(request, year, month):   # 根据年月查询归档文章
    articles = models.Article.objects.filter(create_time__year=year, create_time__month=month)
    return render(request, 'archive_detail.html', {'articles': articles, 'year': year, 'month': month})




