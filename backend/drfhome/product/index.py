from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product

@register(Product)
class YourModelIndex(AlgoliaIndex):
    fields = ('title', 'content','public','price')
    settings = {'searchableAttributes': ['public'],
    'attributesForFaceting': ['filterOnly(public)']}
    tags = 'get_tags_list'

