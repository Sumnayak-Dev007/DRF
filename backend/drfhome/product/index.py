from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Product

@register(Product)
class ProductIndex(AlgoliaIndex):

    def get_queryset(self):
        return Product.objects.filter(public=True)

    


    fields = (
        'title', 
        'content',
        'public',
        'price',
        'sale_price',
        'get_discount',
        'user_username'
    )


    settings = {
        'searchableAttributes': ['title', 'content', 'user_username'],
        'attributesForFaceting': [
            'public',
            'user_username'
        ],
    }


    tags = 'get_tags_list'

    def get_user_username(self, obj):
        try:
            return obj.user.username if obj.user else None
        except Exception as e:
            print(f"[Algolia] Failed to get username for product {obj.pk}: {e}")
            return None
