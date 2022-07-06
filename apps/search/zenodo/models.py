from dataclasses import dataclass, field
from typing import List


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


@dataclass
class ZenodoResponse:
    records: List[ZenodoHit] = field(default_factory=lambda: [ZenodoHit])
    current_page: int = 0
    pages_number: int = 0
