from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product
from django.forms.models import model_to_dict
from product.serializers import ProductSerializers


def echo_get_request(request):
    body = request.body
    data = {}
    try:
        data = json.loads(body)
    except:
        pass
    print(data)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    data['params'] = dict(request.GET) #to get the query parameter from url .com/api/?name=ss
    return JsonResponse(data)




@api_view(['GET','POST'])
def api_home(request, *args, **kwargs):
    instance = Product.objects.all().order_by("?").first()
    print(instance.title)
    data = {}
    if request.method == "GET":
        # data = model_to_dict(model_data)
        data = ProductSerializers(instance).data
        return Response(data)
    elif request.method == "POST":
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({"message":"invalid data"},status=400)

    
def apidemo(request):
    return JsonResponse({"message":"Demooooo"})