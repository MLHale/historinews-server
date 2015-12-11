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

class newspaper_view(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, id=None, format=None):
        if id:
            newspapers = newspaper.objects.filter(id=id)
        else:
            query_params = request.query_params
  
            # check if search text was given
            if 'searchText' not in query_params:
                newspapers = newspaper.objects.all()
            else:
                # sanitize search string
                search_string = query_params['searchText']
                
                newspapers = newspaper.objects.none()
                
                # check if searching all
                search_type = 'all'
                if search_type in query_params and query_params[search_type] == 'true':
                    newspapers |= newspaper.objects.filter(authorName__iregex=search_string)
                    newspapers |= newspaper.objects.filter(keywords__iregex=search_string)
                    newspapers |= newspaper.objects.filter(newspaperCreationDate__iregex=search_string)
                    newspapers |= newspaper.objects.filter(newspaperName__iregex=search_string)
                    newspapers |= newspaper.objects.filter(newspaperTitle__iregex=search_string)
                    newspapers |= newspaper.objects.filter(newspaperYear__iregex=search_string)
                    newspapers |= newspaper.objects.filter(ocrText__iregex=search_string)
                else:
                    search_type = 'authorName'
                    if search_type in query_params and query_params[search_type] == 'true':
                        newspapers |= newspaper.objects.filter(authorName__iregex=search_string)
                    
                    search_type = 'keywords'
                    if search_type in query_params and query_params[search_type] == 'true':
                        newspapers |= newspaper.objects.filter(keywords__iregex=search_string)
                    
                    search_type = 'newspaperCreationDate'
                    if search_type in query_params and query_params[search_type] == 'true':
                        newspapers |= newspaper.objects.filter(newspaperCreationDate__iregex=search_string)
                    
                    search_type = 'newspaperName'
                    if search_type in query_params and query_params[search_type] == 'true':
                        newspapers |= newspaper.objects.filter(newspaperName__iregex=search_string)
                    
                    search_type = 'newspaperTitle'
                    if search_type in query_params and query_params[search_type] == 'true':
                        newspapers |= newspaper.objects.filter(newspaperTitle__iregex=search_string)
                    
                    search_type = 'newspaperYear'
                    if search_type in query_params and query_params[search_type] == 'true':
                        newspapers |= newspaper.objects.filter(newspaperYear__iregex=search_string)
                    
                    search_type = 'ocrText'
                    if search_type in query_params and query_params[search_type] == 'true':
                        newspapers |= newspaper.objects.filter(ocrText__iregex=search_string)


        newspapers_serializer = newspaper_serializer(newspapers, many=True, context={'request': request})
        return Response({
          'newspapers': newspapers_serializer.data,
        })
