from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from historinews.api.models import *
from historinews.api.serializers import *

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