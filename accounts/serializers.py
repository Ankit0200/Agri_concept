from rest_framework import serializers
from . import models
from news_publishing.models import scoreboard
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = ('name','id')


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LocalBody
        fields = '__all__'


class leaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = scoreboard
        fields = '__all__'
