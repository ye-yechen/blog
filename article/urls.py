from django.conf.urls import url
import views
urlpatterns = [
    url(r'^blog/$', views.home),
    url(r'^blog/(?P<page>\d+)$', views.home),
    url(r'^article/publish$', views.publish, name='article_publish'),
    url(r'^article/save$', views.save_article, name='article_save'),
    url(r'^article/detail/(?P<article_id>\d+)$', views.article_detail, name='article_detail'),
]
