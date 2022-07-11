from rest_framework import generics
from rest_framework.response import Response
from .serializers import NewsSerializer
from .models import News


class NewsCreateApi(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsListApi(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDeleteApi(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
