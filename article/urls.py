from django.conf.urls import url
import views
from views import RegisterView
urlpatterns = [
    url(r'^blog/$', views.home),
    url(r'^blog/(?P<page>\d+)$', views.home),
    url(r'^article/publish$', views.publish, name='article_publish'),
    url(r'^article/save$', views.save_article, name='article_save'),
    url(r'^article/detail/(?P<article_id>\d+)$', views.article_detail, name='article_detail'),
    url(r'^accounts/register$', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.active_user, name='active_user'),
    url(r'^accounts/loginpage$', views.login_page, name='login'),
    url(r'^accounts/login$', views.login_site, name='login_site'),
    url(r'^accounts/logout$', views.logout_site, name='logout'),
    url(r'^article/reply/(?P<article_id>\d+)$', views.reply, name='reply'),
    url(r'^article/archive$', views.archive, name='archive'),
    url(r'^article/archive/(?P<year>\d+)/(?P<month>\d+)/(?P<page>\d+)$', views.search_archive, name='search_archive'),
    url(r'^article/category/(?P<category_name>.+)/(?P<page>\d+)$', views.search_category, name='search_category'),
    url(r'^article/tag/(?P<tag_name>.+)/(?P<page>\d+)$', views.search_tag, name='search_tag'),
]
