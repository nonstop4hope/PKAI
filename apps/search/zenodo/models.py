from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass
class HitCreator:
    affiliation: str = ''
    name: str = ''


@dataclass
class ZenodoHit:
    title: str = ''
    description: str = ''
    publication_date: str = ''
    keywords: List[str] = field(default_factory=lambda: [])
    link: str = ''
    access_right: str = ''
    creators: List[HitCreator] = field(default_factory=lambda: [HitCreator])


@dataclass_json
@dataclass
class ZenodoResponse:
    records: List[ZenodoHit] = field(default_factory=lambda: [ZenodoHit])
    current_page: int = 0
    pages_number: int = 0
