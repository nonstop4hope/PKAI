from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.views import APIView

from PKAI.settings import TARGET_MAIL_BOX
from .serializers import ContactSerializer


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            username = data.get('username')
            from_email = data.get('email')
            phone = data.get('phone')
            message = data.get('message')
            send_mail(f'От {username} | {phone}', message, from_email, [TARGET_MAIL_BOX])
            return JsonResponse({'status': 'sent'})
        else:
            return JsonResponse(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
