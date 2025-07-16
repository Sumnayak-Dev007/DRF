from rest_framework import viewsets, mixins
from .models import Product
from .serializers import ProductSerializers


class ProductViewset(viewsets.ModelViewSet):
    """
    get -> list -> Queryset  
    get -> retrieve -> Product Instance Detail View  
    post -> create -> New Instance  
    put -> Update  
    patch -> Partial Update  
    delete -> destroy  
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    get -> list -> Queryset  
    get -> retrieve -> Product Instance Detail View  
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'  # default
