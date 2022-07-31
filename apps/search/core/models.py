from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass
class HitCreator:
    affiliation: str = ''
    name: str = ''


@dataclass
class CoreHit:
    title: str = ''
    description: str = ''
    publication_date: str = ''
    keywords: List[str] = field(default_factory=lambda: [])
    link: str = ''
    access_right: str = ''
    creators: List[HitCreator] = field(default_factory=lambda: [HitCreator])


@dataclass_json
@dataclass
class CoreResponse:
    records: List[CoreHit] = field(default_factory=lambda: [CoreHit])
    current_page: int = 0
    total_records: int = 0
