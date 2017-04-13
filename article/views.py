# -*- coding:utf-8 -*-
from django.db.models import Count
from django.shortcuts import render
import models
from models import Article, Reply, Tag, Category, Message
import markdown
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from forms import RegisterForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings as django_settings
from token import token_confirm
from collections import defaultdict, OrderedDict
from tag_cloud import TagCloud, TagInfo


# def get_tag_article_nums():    # 查询各标签以及含此标签的文章数量
#     tags = Tag.objects.annotate(articles_count=Count('article'))
#     return tags


def get_tag_info():     # 封装标签信息
    tag_list = Tag.objects.annotate(articles_count=Count('article'))  # 统计标签制作标签云
    tag_info_list = []
    max_ref = 0
    min_ref = float('inf')
    for tag in tag_list:
        if tag.articles_count > max_ref:
            max_ref = tag.articles_count
        if tag.articles_count < min_ref:
            min_ref = tag.articles_count

    tag_cloud = TagCloud(min_ref, max_ref)
    for tag in tag_list:
        tag_size = tag_cloud.get_tag_font_size(tag.articles_count)
        tag_color = tag_cloud.get_tag_color(tag.articles_count)
        tag_info = TagInfo(tag.tag_name, tag_size, tag_color, tag.articles_count)
        tag_info_list.append(tag_info)
    return tag_info_list


def home(request, page=1):
    articles = Article.objects.all().order_by('-create_time')
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

    tag_info_list = get_tag_info()

    return render(request, 'index.html', {'html_title': '首页', 'articles': articles, 'tag_info_list': tag_info_list})


def publish(request):   # 发表文章
    if not request.user.is_authenticated():  # 用户未登录，不能发表文章
        return render(request, 'login.html')
    categories = Category.objects.all()  # 查询所有分类
    return render(request, 'publish.html', {'categories': categories})


def save_tags(tags):    # 构造标签,返回标签类列表
    tag_names = tags.split()
    now = datetime.datetime.now()
    tag_list = []
    for tag_name in tag_names:
        # 查询数据库是否有这个tag(不能用get方法，因为如果数据库无记录，get方法会报错)
        tag = Tag.objects.filter(tag_name=tag_name)
        if tag:
            tag_list.append(tag[0])
        else:
            tag = Tag.objects.create(
                tag_name=tag_name,
                create_time=now
            )
            tag_list.append(tag)
    return tag_list


def save_article(request):  # 保存文章
    if not request.user.is_authenticated():  # 用户未登录，不能发表文章
        return render(request, 'login.html')
    title = request.POST.get('title')
    content_md = request.POST.get('content')
    category_name = request.POST.get('category')
    category = Category.objects.get(category_name=category_name)  # 根据名称查找分类
    tags = request.POST.get('tags')
    content_html = markdown.markdown(content_md)
    now = datetime.datetime.now()
    create_time = now
    update_time = now
    summary = content_md[:50]
    article = Article.objects.create(
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
    # 构造标签对象
    tag_list = save_tags(tags)
    for tag in tag_list:    # 依次给文章添加标签
        article.tags_2.add(tag)
    article.save()
    articles = Article.objects.all().order_by('-create_time')
    tag_info_list = get_tag_info()
    for article in articles:
        article.tags = article.tags.split()
    return render(request, 'index.html', {'html_title': '首页', 'articles': articles, 'tag_info_list': tag_info_list})


def article_detail(request, article_id):  # 全文阅读
    article = Article.objects.get(pk=article_id)  # 查找博客
    article.read_count += 1  # 阅读次数+1
    article.save()
    article.tags = article.tags.split()

    replies = models.Reply.objects.filter(article_id=article_id)  # 查找此博客的所有回复
    tag_info_list = get_tag_info()
    # for reply in replies:
    #     print reply.author.username
    return render(request, 'article_detail.html', {'article': article, 'replies': replies, 'tag_info_list': tag_info_list})


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
        article = Article.objects.get(pk=article_id)  # 获取此文章
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
            Reply.objects.create(
                content=content,
                author=author,
                article=article,
                reply_time=reply_time
            )
            article.comment_nums += 1  # 文章评论数+1
            article.save()

        article.tags = article.tags.split()
        replies = Reply.objects.filter(article_id=article_id)  # 查找此博客的所有回复
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
    date_list = Article.objects.datetimes('create_time', 'month', order='DESC')
    article_dict = OrderedDict()
    for date in date_list:
        year = int(date.year)
        month = int(date.month)
        article_list = Article.objects.filter(create_time__year=year, create_time__month=month)
        # article_dict.setdefault(date, []).append(article_list)
        article_dict[date] = article_list
    return render(request, 'archive.html', {'data_list': date_list, 'article_dict': article_dict})


def search_archive(request, year, month, page=1):   # 根据年月查询归档文章
    articles = Article.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
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
    return render(request, 'archive_detail.html', {'articles': articles, 'year': year, 'month': month})


def search_category(request, category_name, page=1):    # 搜索相同分类的文章并分页显示
    # category_name = category_name.decode().encode('utf-8')
    # category = Category.objects.get(category_name=category_name)
    # articles = Article.objects.filter(category=category)
    articles = Category.objects.get(category_name=category_name).article_set.all().order_by('-create_time')  # 此语句与以上两条等效
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

    tag_info_list = get_tag_info()
    return render(request, 'index.html', {'html_title': category_name, 'articles': articles, 'tag_info_list': tag_info_list})


def search_tag(request, tag_name, page=1):  # 搜索相同标签的文章并分页显示
    articles = Tag.objects.get(tag_name=tag_name).article_set.all().order_by('-create_time')
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

    tag_info_list = get_tag_info()
    return render(request, 'index.html', {'html_title': tag_name, 'articles': articles, 'tag_info_list': tag_info_list})


def about(request):     # 关于页面
    return render(request, 'about.html')


def message_board(request):     # 留言页面
    if request.method == 'POST':
        message_content = request.POST.get('message_content')
        Message.objects.create(
            content=message_content,
            author=request.user,
            message_time=datetime.datetime.now()
        )
    messages = Message.objects.all().order_by('-message_time')
    return render(request, 'message_board.html', {'messages': messages})


