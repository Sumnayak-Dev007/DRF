from rest_framework import generics
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializers
from algoliasearch.search.client import SearchClientSync 

client = SearchClientSync("8H1FCJWZWP", "641ca1e39b3a0738fe4378e475599fd7")

class SearchListView(generics.GenericAPIView):
    queryset = [] 

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if not query:
            return Response({'error': 'Query parameter "q" is required.'}, status=400)

        try:
            response = client.search({
                "requests": [
                    {
                        "indexName": "suman_Product",
                        "query": query,
                        "hitsPerPage": 50,
                    },
                ],
            })

            response_dict = response.to_dict()
            hits = response.to_dict()['results'][0]['hits']

            cleaned_hits = []
            for hit in hits:
                cleaned_hit = {
                    "objectID": hit.get("objectID"),
                    "title": hit.get("title"),
                    "content": hit.get("content"),
                    "public": hit.get("public"),
                    "price": hit.get("price"),
                    "sale_price": hit.get("sale_price"),
                    "discount": hit.get("get_discount"),
                    "user_username": hit.get("user_username"),
                    "_tags": hit.get("_tags", []),
                    "highlighted_title": hit.get("_highlightResult", {}).get("title", {}).get("value"),
                    "highlighted_user": hit.get("_highlightResult", {}).get("user_username", {}).get("value"),
                }
                cleaned_hits.append(cleaned_hit)

            return Response(cleaned_hits)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            results = qs.search(q)
        else:
            results = qs.filter(public=True)  # Also show only public if no query
        return results

# Create your views here.
