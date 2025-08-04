from rest_framework import generics
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializers

# from . import client
# class SearchListView(generics.GenericAPIView):
#     def get(self, request, *args, ** kwargs):
#         query = request.GET.get('q')
#         if not query:
#             return Response('', status=400)
#         results = client.perform_search(query)
#         return Response(results)

class SearchListView(generics.ListAPIView):
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
