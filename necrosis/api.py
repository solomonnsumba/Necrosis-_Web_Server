import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ApiSerializer
from .models import Api_Images
from .views import BASE_DIR
from .cbsdanalyzer import *
import base64
import os


@csrf_exempt
@api_view(['POST', 'GET'])
def upload_image(request):
	if request.method == 'POST':
		serializer =  ApiSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		querryset = Api_Images.objects.all()
		serializer = ApiSerializer(querryset, many=True)
		return Response(serializer.data)



class ApiViewset(viewsets.ViewSet):
	"""
	create:
	      Upload Image 
	"""
	serializer_class = ApiSerializer


	def create(self, request):
		serializer = ApiSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			obj = serializer.data
			img = resize_images(obj['image'])
			img1, img1_name, img_cbsd_score = analyze_image(img)

			
			encoded_image = base64.b64encode(open(fpath, "rb").read())

			res = {"image_name": os.path.split(img1_name)[1], "cbsd_score": img_cbsd_score, "image_link": "http://18.219.45.102/static/results/"+os.path.split(img1_name)[1]}
			
			return Response(res, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		

def encode_image(img_path):
	with open(img_path, "rb") as image_file:
		encoded_image = base64.b64encode(image_file.read())