from rest_framework import serializers

#load django and webapp models
from django.contrib.auth.models import *
from historinews.api.models import *

class article_serializer(serializers.ModelSerializer):
    class Meta:
        model = article
        fields = ('keywords', 'newspaperName', 'newspaperYear', 'articleTitle', 'authorName', 'articleCreationDate', 'ocrText', 'pdfLocation')
