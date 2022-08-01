from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .views import get_celery_result_by_id, get_core_records
import json
from django.test import TestCase


class CoreTest(TestCase):
    factory = APIRequestFactory()
    user = User.objects.get(username='test')

    request = factory.get('/api/v1/search/core?query=test&page=5586')
    request.user = user
    force_authenticate(request, user=user)
    response = get_core_records(request)
    print(response.content)
    content = json.loads(response.content)
    task_id = content.get('task_id')

    task_status = "PENDING"

    while True:
        request = factory.get(f'/api/v1/search/result?task_id={task_id}')
        request.user = user
        force_authenticate(request, user=user)
        response = get_celery_result_by_id(request)
        content = json.loads(response.content)
        task_status = content.get("task_status")

        if task_status != "PENDING":
            break

    print(response.content)
