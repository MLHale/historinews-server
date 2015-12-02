from django.conf.urls import include, url

#Django Rest Framework
from rest_framework import routers
from historinews.api import views
from rest_framework.urlpatterns import format_suffix_patterns

#REST API routes
router = routers.DefaultRouter()
#router.register(r'posts', views.PostViewSet) #use this for viewset approach
router.register(r'articles', views.article_view_set)

#REST API
urlpatterns = [
    url(r'^', include(router.urls)),

    #class-based view approach
    #url(r'^$', views.api_root), #needed if you use all class-based views and want them to show up in the landing page for the browsable api
    #url(r'^posts/$', views.PostList.as_view(), name='post-list'),
    #url(r'^posts/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='post-detail'),
]