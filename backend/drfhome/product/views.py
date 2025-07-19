from rest_framework import authentication,generics,mixins,permissions
from .models import Product
from rest_framework import status
from .serializers import ProductSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.authentication import TokenAuthentication
from api.permissions import IsStaffEditorPermission
from api.mixins import (
    UserQuerySetMixin,
    IsStaffEditorPermissionMixins,
    )
from api.mixins import IsStaffEditorPermissionMixins




class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content=content)

class ProductAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class PostAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    

    def perform_create(self,serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content = content)

class ListCreateAPIView(
    UserQuerySetMixin,
    IsStaffEditorPermissionMixins,
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    authentication_classes = [
    authentication.SessionAuthentication,
    TokenAuthentication
    ]

    def perform_create(self,serializer):
        email = serializer.validated_data.pop('email')
        print(email)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user,content = content)


    # def get_queryset(self,*args,**kwargs):
    #     qs = super().get_queryset(*args,**kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     print(request.user)
    #     return qs.filter(user = request.user)
    



    
# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers

class PutAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_fiels = 'pk'

    def perform_update(self,serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


class DeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Product deleted successfully."},
            status=status.HTTP_200_OK
        )

    def perform_destroy(self,instance):
        super().perform_destroy(instance)


#----------Function Based---------------
@api_view(['GET','POST'])
def list_create_all(request,pk=None,*args,**kwargs):
    if request.method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product,pk=pk)
            data = ProductSerializers(obj,many=False).data 
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializers(queryset,many=True).data 
        return Response(data)
    elif request.method == "POST":
        data = request.data 
        serializer = ProductSerializers(data=data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content = content)
            return Response(serializer.data)
        return Response({"message":"Not Good Data :("},status=400)
