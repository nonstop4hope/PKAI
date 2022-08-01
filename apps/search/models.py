from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass
class HitCreator:
    affiliation: str = ''
    name: str = ''


@dataclass
class Hit:
    title: str = ''
    description: str = ''
    publication_date: str = ''
    keywords: List[str] = field(default_factory=list)
    link: str = ''
    access_right: str = ''
    creators: List[HitCreator] = field(default_factory=list)


@dataclass_json
@dataclass
class ApiResult:
    records: List[Hit] = field(default_factory=list)
    current_page: int = 0
    total_records: int = 0
    message: str = ''
