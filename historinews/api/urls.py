from django.conf.urls import include, url

#Django Rest Framework
from rest_framework import routers
from historinews.api import views
from rest_framework.urlpatterns import format_suffix_patterns

#REST API routes
router = routers.DefaultRouter()

#REST API
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^articles/?', views.article_view.as_view()),
    url(r'^articles/(?P<id>\d+)/?', views.article_view.as_view()),
]