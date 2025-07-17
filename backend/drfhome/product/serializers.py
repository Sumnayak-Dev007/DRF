from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product

class ProductSerializers(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
            view_name='product-details',
            lookup_field='pk')
    
    
    class Meta:
        model = Product
        fields = [
            'edit_url',
            'url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount'
        ]

    def get_edit_url(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit",kwargs={"pk":obj.pk},request=request)


    def get_my_discount(self,obj):
        return obj.get_discount()