from rest_framework import serializers
from .models import Api_Images


class ApiSerializer(serializers.ModelSerializer):
	image  = serializers.FileField()

	class Meta:
		model = Api_Images
		fields = '__all__'