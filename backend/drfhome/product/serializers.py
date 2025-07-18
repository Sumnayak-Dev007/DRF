from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product

class ProductSerializers(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
            view_name='product-details',
            lookup_field='pk')
    email = serializers.EmailField(write_only=True)
    # name = serializers.CharField(source='title',read_only=True)

    
    class Meta:
        model = Product
        fields = [
            'edit_url',
            'url',
            'email',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount'
        ]


    def validate_title(self,value):
        qs = Product.objects.filter(title__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(f'{value} is already a product name')
        return value
    
    def create(self, validated_data):
        email = validated_data.pop('email', None)
        obj = super().create(validated_data)
        if email:
            print(f"Email captured: {email}")
        return obj


    def update(self,instance,validated_data):
        email = validated_data.pop('email')
        return super().update(instance,validated_data)


    def get_edit_url(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit",kwargs={"pk":obj.pk},request=request)


    def get_my_discount(self,obj):
        return obj.get_discount()