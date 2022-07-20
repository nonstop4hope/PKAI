import dataclasses
from dataclasses import dataclass
from typing import Dict

from PKAI.celery import app
from apps.search.zenodo.models import ZenodoResponse


@dataclass
class CeleryZenodoResponse:
    task_id: str = ''
    task_status: str = ''
    task_result: ZenodoResponse = None


def get_task_state_by_id(task_id: str) -> Dict:
    task = app.AsyncResult(task_id)
    response = CeleryZenodoResponse(task_id=task_id, task_status=task.status, task_result=task.result)
    return dataclasses.asdict(response)

