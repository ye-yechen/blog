from django.conf.urls import url
import views
from views import RegisterView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^blog/$', views.home, name='index'),
    url(r'^blog/(?P<page>\d+)$', views.home, name='blog_index'),
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
    url(r'^blog/about', views.about, name='about'),
    url(r'^blog/photos', views.photo_wall, name='photo_wall'),
    url(r'^blog/upload', views.upload_img, name='upload_img'),
    url(r'^blog/message', views.message_board, name='message_board'),
    url(r'^blog/show$', views.zhihu_style, name='zhihu_style'),
    url(r'^blog/usernum$', views.get_user_num, name='get_user_num'),
    url(r'^blog/sex$', views.get_sex, name='get_sex'),
    url(r'^blog/school$', views.get_school_count, name='get_school_count'),
    url(r'^blog/business$', views.get_business_count, name='get_business_count'),
    url(r'^blog/location$', views.get_location_count, name='get_location_count'),
    url(r'^blog/company$', views.get_company_count, name='get_company_count'),
    url(r'^blog/voteup$', views.get_voteup_count, name='get_voteup_count'),
    url(r'^blog/follower$', views.get_follower_count, name='get_follower_count'),
    url(r'^blog/answer$', views.get_answer_count, name='get_answer_count'),
    url(r'^blog/name$', views.get_name_count, name='get_name_count'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

