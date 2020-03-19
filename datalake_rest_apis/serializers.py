from rest_framework import serializers
from .models import RawDataFile


class RawDataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawDataFile
        fields = '__all__'  # ('id', 'title', 'path')
