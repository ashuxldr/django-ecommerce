from rest_framework import viewsets
from .serializers import *
from .models import *
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
