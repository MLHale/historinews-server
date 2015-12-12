from django.shortcuts import render, render_to_response
from django.shortcuts import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from historinews.api.models import *
from historinews.api.serializers import *
import calendar
import datetime
import re


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

#date_regex = re.compile(r'^(\d+)[\/-](\d+)$')
date_regex = re.compile(r'^(\d+)[\/-](\d+)[\/-](\d+)$') # MM-DD-YYYY
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
                    newspapers |= newspaper.objects.filter(_keywords__iregex=search_string)
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
                        newspapers |= newspaper.objects.filter(_keywords__iregex=search_string)
                    
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

            # set startDate if exists
            startDate = False
            if 'startDate' in query_params:
                # MM-DD-YYYY
                result = date_regex.match(query_params['startDate'])
                if result:
                    result = result.groups()
                    #month, year = (int(i) for i in result)
                    month, day, year = (int(i) for i in result)
                    if month < 1:
                        month = 1
                    if month > 12:
                        month = 12
                    day = 1
                    startDate = year, month, day

            # set endDate if exists
            endDate = False
            if 'endDate' in query_params:
                # MM-DD-YYYY
                result = date_regex.match(query_params['endDate'])
                if result:
                    result = result.groups()
                    #month, year = (int(i) for i in result)
                    month, day, year = (int(i) for i in result)
                    if month < 1:
                        month = 1
                    if month > 12:
                        month = 12
                    day = calendar.monthrange(year, month)[1]
                    endDate = year, month, day

            # check for period
            if 'period' in query_params and query_params['period']:
                era_newspapers = newspaper.objects.none()
                periods = query_params['period'].split('|')
                for period in periods:
                    if period.lower() == 'gilded age':
                        era_newspapers |= newspapers.filter(newspaperCreationDate__gt=datetime.date(1870, 1, 1), newspaperCreationDate__lt=datetime.date(1900, 12, 31))
                    elif period.lower() == 'progressive era':
                        era_newspapers |= newspapers.filter(newspaperCreationDate__gt=datetime.date(1890, 1, 1), newspaperCreationDate__lt=datetime.date(1920, 12, 31))
                    elif period.lower() == 'korean war':
                        era_newspapers |= newspapers.filter(newspaperCreationDate__gt=datetime.date(1939, 1, 1), newspaperCreationDate__lt=datetime.date(1939, 12, 31))
                    elif period.lower() == 'world war ii':
                        era_newspapers |= newspapers.filter(newspaperCreationDate__gt=datetime.date(1950, 1, 1), newspaperCreationDate__lt=datetime.date(1950, 12, 31))

                # check for start and end dates after era taken into account
                if startDate and endDate:
                    era_newspapers |= newspapers.filter(newspaperCreationDate__gt=datetime.date(*startDate), newspaperCreationDate__lt=datetime.date(*endDate))
                elif startDate and not endDate:
                    era_newspapers |= newspapers.filter(newspaperCreationDate__gt=datetime.date(*startDate))
                elif endDate and not startDate:
                    era_newspapers |= newspapers.filter(newspaperCreationDate__lt=datetime.date(*endDate))
                newspapers = era_newspapers
            else:
                # otherwise just check start and end date
                if startDate and endDate:
                    newspapers = newspapers.filter(newspaperCreationDate__gt=datetime.date(*startDate), newspaperCreationDate__lt=datetime.date(*endDate))
                elif startDate and not endDate:
                    newspapers = newspapers.filter(newspaperCreationDate__gt=datetime.date(*startDate))
                elif endDate and not startDate:
                    newspapers = newspapers.filter(newspaperCreationDate__lt=datetime.date(*endDate))

            # check for newspaper name
            if 'name' in query_params and query_params['name']:
                named_newspapers = newspaper.objects.none()
                names = query_params['name'].split('|')
                for name in names:
                    named_newspapers |= newspapers.filter(newspaperName__iexact=name)
                newspapers = named_newspapers

        newspapers_serializer = newspaper_serializer(newspapers, many=True, context={'request': request})
        return Response({
          'newspapers': newspapers_serializer.data,
        })
