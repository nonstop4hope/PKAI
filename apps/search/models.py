from typing import List

from django.contrib.postgres.fields import ArrayField
from django.db import models
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


class File(BaseModel):
    checksum: str = ''
    key: str = ''
    link: str = ''
    size: int = 0
    type: str = ''


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


class HitAuthor(models.Model):
    affiliation = models.TextField(default=None, null=True)
    name = models.TextField(default=None, blank=True)


class GeneralizedHitsSearch(models.Model):

    query = models.TextField(default=None)
    source = models.CharField(max_length=255)
    source_id = models.BigIntegerField()
    title = models.TextField()
    description = models.TextField(null=True, default=None, blank=True)
    full_text = models.TextField(null=True, blank=True, default=None)
    doi = models.CharField(max_length=255, default=None, null=True)
    type = models.CharField(max_length=255, default=None, null=True)
    language = models.CharField(max_length=255, default=None, null=True)
    publication_date = models.DateTimeField(default=None, null=True)
    source_keywords = ArrayField(models.CharField(max_length=255, blank=True), default=list, blank=True)
    original_url = models.CharField(max_length=255, default=None, null=True)
    access_right = models.CharField(max_length=255, default=None, null=True)
    citations_number = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(HitAuthor, related_name='hits_list', blank=True)
