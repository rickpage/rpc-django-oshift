from rest_framework import serializers
from .models import *
from pdb import set_trace
from rest_framework.decorators import detail_route


class ProductSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = [
          'id',
          'title',
          'default_price'
        ]


class CompleteProductQuantitySerializer(serializers.ModelSerializer):

    inventory = serializers.ReadOnlyField(source="inventory.id")
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductQuantity
        fields = [
          'id',
          'quantity',
          'product',
          'inventory',
        ]

    def partial_update(self, instance, validated_data, *args, **kwargs):
        # set_trace()
        # Can only change quantity
        instance.quantity = validated_data.get("quantity", instance.quantity)
        return instance

class ProductQuantitySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductQuantity
        fields = [
          'id',
          'quantity',
          'product',
        ]


class InventorySerializer(serializers.ModelSerializer):

    quantities = ProductQuantitySerializer(many=True,read_only=False)

    class Meta:
        model = Inventory
        fields = [
          'id',
          'title',
          'quantities',
        ]

    def create(self, validated_data):
        #u = validated_data.pop('creator')
        qs = validated_data.pop('quantities')
        obj = Inventory.objects.create(**validated_data)
        for pq_data in qs:
            ProductQuantity.objects.create(inventory=obj, **pq_data)
        return obj

    def update(self, instance, validated_data):
        """If we update the inventory, we provide a new quantities entirely.
        This is not always desireable.
        We also need to destroy the old values.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        qs = validated_data.pop('quantities')

        if qs:
            # Get rid of items in qs as they match existing quantities on instance
            # and also drop pqs that are on instance now, but not on pqs
            for current_pq in instance.quantities.all():
                # If this product quantity pointing to inventory
                # is not present in qs, we drop it
                # IF found then overwrite the save
                found = False
                for d in qs:
                    if current_pq.product == d.get("product"):
                        found = True
                        current_pq.quantity = d.get("quantity")
                        current_pq.save()
                        break
                if not found:
                    current_pq.delete()
                # if not any(current_pq.product == d.get("product") for d in qs):
                #     current_pq.delete()
                # else:
                #     # Since it is in here, we can replace data
                #     current_pq.quantity = qs.get(product=current_pq.product)[0].quantity
                # current_pq.save()
        else:
            # delete all the pqs
            instance.quantities.all().delete()
            # for item in qs:
            #     product_id = item.get('product', None)
            #     if product_id:
            #         inv_item = ProductQuantity.objects.get(product=product_id, inventory=instance)
            #         inv_item.quantity = item.get('quantity', inv_item.quantity)
            #         inv_item.save()
            #     else:
            #         ProductQuantity.objects.create(inventory=instance, **item)

        return instance


    @detail_route(methods=['post'], permission_classes=[])
    def add(self, request, pk=None):
        """Keep old values, and add the quantity of passed in PQ-like models
        """
        #instance.title = validated_data.get("title", instance.title)
        #instance.save()
        if pk is None:
            raise ValidationError("Provide inventory id to add to")

        qs = ProductQuantitySerializer(request.data.pop('quantities'))

        if qs:
            for item in qs:
                product_id = item.get('product', None)
                if product_id:
                    inv_item = ProductQuantity.objects.get(product=product_id, inventory=instance)
                    inv_item.quantity = inv_item.quantity + item.get('quantity', inv_item.quantity)
                    inv_item.save()
                else:
                    ProductQuantity.objects.create(inventory=instance, **item)

        return instance

"""
To help edit Inventory objects without using quantity/<pk> PATCH/PUT,
especially to edit in bulk operation.
"""

"""
INTERNAL
"""
class EditQuantity():
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

class EditQuantitySerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(default=0)

    def create(self, validated_data):
        """
        Returns inventory edit object, which Inventory will use internally
        """
        return EditQuantity(**validated_data)

class InventoryEditorSerializer(serializers.Serializer):
    # inventory_id = serializers.IntegerField() # We would want this as a PK argument
    add = EditQuantitySerializer(many=True)

    def create(self, validated_data):
        """
        Create doesn't apply
        """
        return {}

    def update(self, instance, validated_data):
        """

        """
        return {}
