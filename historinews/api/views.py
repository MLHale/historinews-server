from django.shortcuts import *

# Import models
from django.db import models
from django.contrib.auth.models import *
from historinews.api.models import *

#REST API
from rest_framework import viewsets
from historinews.api.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class article_view_set(viewsets.ModelViewSet):
    """
    API endpoint that allows for CRUD operations on post objects.
    """
    queryset = article.objects.all()
    serializer_class = article_serializer