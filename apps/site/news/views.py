from rest_framework import generics

from .models import News
from .serializers import NewsSerializer


class NewsCreateApi(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class NewsListApi(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class NewsUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class NewsDeleteApi(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (permissions.IsAuthenticated,)
