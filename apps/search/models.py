from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json
from pydantic import BaseModel


@dataclass
class Author:
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
    creators: List[Author] = field(default_factory=list)


@dataclass_json
@dataclass
class ApiResult:
    records: List[Hit] = field(default_factory=list)
    current_page: int = 0
    total_records: int = 0
    message: str = ''


class CitationHit(BaseModel):
    title: str = ''
    authors: List[Author] = []
    doi: str = ''
    url: str = ''
    type: str = ''
    date: str = ''
    language: str = ''


class GeneralizedHit(BaseModel):
    source: str = ''
    title: str = ''
    description: str = ''
    doi: str = ''
    type: str = ''
    language: str = ''
    publication_date: str = ''
    ISSN: List[str] = ''
    source_keywords: List[str] = []
    auto_generated_keywords: List[str] = []
    original_url: str = ''
    access_right: str = ''
    authors: List[Author] = []
    citations_number: int = 0
    citations: List[CitationHit] = []


class ApiResponse(BaseModel):
    hits: List[GeneralizedHit] = []
    total_records: int = 0
