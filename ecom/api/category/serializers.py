from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'description']