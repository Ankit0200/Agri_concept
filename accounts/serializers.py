from rest_framework import serializers
from . import models

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = ('name','id')


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LocalBody
        fields = '__all__'

