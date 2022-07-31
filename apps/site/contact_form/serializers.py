from rest_framework import serializers

from apps.site.contact_form.models import FeedbackRecord


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackRecord
        fields = ('username', 'email', 'phone', 'message')

# class ContactSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=200)
#     email = serializers.CharField(max_length=200)
#     phone = PhoneNumberField(blank=True, null=True, unique=False)
#     message = serializers.CharField(max_length=2000)
