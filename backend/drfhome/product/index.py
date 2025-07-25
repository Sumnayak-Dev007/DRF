import algoliasearch_django as algoliasearch

from .models import Product

algoliasearch.register(Product)