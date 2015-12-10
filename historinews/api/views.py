from django.shortcuts import render, render_to_response
from django.shortcuts import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from historinews.api.models import *
from historinews.api.serializers import *

def home(request):
  """
  Sends requests to / to the ember.js clientside app
  """
  return render_to_response('index.html', {}, RequestContext(request))


def robots(request):
  """
  Allows access to /robots.txt
  """
  return render(request, 'robots.txt', {},  content_type="text/plain")


def crossdomain(request):
  """
  Allows access to /crossdomain.xml
  """
  return render(request, 'crossdomain.xml', {},  content_type="application/xml")

class article_view(APIView):
    permission_classes = (AllowAny,)
    serializer_class = article_serializer
    
    def get(self, request, id=None, format=None):
        if id:
            articles = article.objects.filter(id=id)
        else:
            articles = article.objects.all()
        
        # Serialize team object and return the serialized data.
        articles_serializer = article_serializer(articles, many=True, context={'request': request})
        return Response({
          "articles": articles_serializer.data,
        })
class newspaper_view(APIView):
    permission_classes = (AllowAny,)
    serializer_class = article_serializer
    
    def get(self, request, id=None, format=None):
        if id:
            articles = article.objects.filter(id=id)
        else:
            articles = article.objects.all()
        
        # Serialize team object and return the serialized data.
        articles_serializer = article_serializer(articles, many=True, context={'request': request})
        return Response({
          "articles": articles_serializer.data,
        })