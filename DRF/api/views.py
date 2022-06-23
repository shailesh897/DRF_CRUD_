from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer


@api_view(["GET"])
def ApiOverview(request):
    api_urls = {
        "all_items": "/",
        "Search by Category": "/?category=category_name",
        "Search by Subcategory": "/?subcategory=category_name",
        "Add": "/create",
        "Update": "/update/pk",
        "Delete": "/item/pk/delete",
    }

    return Response(api_urls)

@api_view(['POST'])
def add_items(request):
	item = ItemSerializer(data=request.data)
	# if already existing data
	if Item.objects.filter(**request.data).exists():
		raise serializers.ValidationError('This data already exists')

	if item.is_valid():
		item.save()
		return Response(item.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_items(request):
	# checking for the parameters from the URL
	if request.query_params:
		items = Item.objects.filter(**request.query_param.dict())
	else:
		items = Item.objects.all()

	# if there is something in items else raise error
	if items:
		data = ItemSerializer(items)
		return Response(data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)


    