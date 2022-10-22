from typing import List


from pydantic import BaseModel


class Author(BaseModel):
    affiliation: str = ''
    name: str = ''


class Hit(BaseModel):
    title: str = ''
    description: str = ''
    publication_date: str = ''
    keywords: List[str] = []
    link: str = ''
    access_right: str = ''
    creators: List[Author] = []


class ApiResult(BaseModel):
    records: List[Hit] = []
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
    id: str = ''
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


class CitationsShort(BaseModel):
    number: int = 0
    doi_list: List[str] = []


class CrossrefInfo(BaseModel):
    doi: str = ''
    url: str = ''
    title: str = ''
    authors: List[Author] = []