from rest_framework import generics
from rest_framework import permissions
from .serializers import NewsSerializer
from .models import News


class NewsCreateApi(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NewsListApi(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NewsUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NewsDeleteApi(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (permissions.IsAuthenticated,)
