from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import GeneralizedHitsSearch


@registry.register_document
class HitDocument(Document):
    authors = fields.ObjectField(properties={
        'affiliation': fields.TextField(),
        'name': fields.TextField(),
        'creation_date': fields.DateField(),
    })

    related_identifiers = fields.ObjectField(properties={
        'scheme': fields.TextField(),
        'identifier': fields.TextField(),
    })

    source_keywords = fields.ListField(fields.TextField())

    class Index:
        name = 'hit'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,

        }

    class Django:
        model = GeneralizedHitsSearch
        fields = [
            'id',
            'source',
            'source_id',
            'title',
            'description',
            'full_text',
            'doi',
            'type',
            'language',
            'publication_date',
            'original_url',
            'access_right',
            'citations_number',
            'creation_date',
        ]
