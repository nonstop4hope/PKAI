from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News
from .serializers import NewsSerializer


class NewsCreateApi(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class NewsListApi(generics.ListAPIView):
    serializer_class = NewsSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = News.objects.all()
        return queryset.order_by('publication_date').reverse()


class NewsOneApi(APIView):
    # serializer_class = NewsSerializer
    #
    # def get_queryset(self):
    #     return News.objects.filter(pk=self.kwargs['news_id'])

    def get(self, request, news_id, *args, **kwargs):

        try:
            instance = News.objects.get(pk=self.kwargs['news_id'])
        except News.DoesNotExist:
            return Response(
                {"res": "Object with news id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NewsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewsUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class NewsDeleteApi(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (permissions.IsAuthenticated,)
