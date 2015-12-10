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
    url(r'^newspapers/?', views.newspaper_view.as_view()),
    url(r'^newspapers/(?P<id>\d+)/?', views.newspaper_view.as_view()),
]