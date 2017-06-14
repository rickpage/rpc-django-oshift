from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = (IsAdminOrIsSelf,)

    # def perform_create(self, serializer):
    #     creator = self.request.user
    #     serializer.save(creator=creator)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProductQuantityViewSet(viewsets.ModelViewSet):
    queryset = ProductQuantity.objects.all()
    serializer_class = CompleteProductQuantitySerializer
    #permission_classes = (IsAdminOrIsSelf,)

    # def perform_create(self, serializer):
    #     creator = self.request.user
    #     serializer.save(creator=creator)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = () # Override is Authenticated permission

    # def perform_create(self, serializer):
    #     creator = self.request.user
    #     serializer.save(creator=creator)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
