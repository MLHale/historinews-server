from rest_framework import serializers
from historinews.api.models import newspaper

class newspaper_serializer(serializers.ModelSerializer):
    class Meta:
        model = newspaper
        fields = ('id', 'keywords', 'newspaperName', 'newspaperYear', 'newspaperTitle',
                  'authorName', 'newspaperCreationDate', 'ocrText', 'pdfLocation', 'thumb')
