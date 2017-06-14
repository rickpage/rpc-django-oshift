from django.test import TestCase
from django.core.urlresolvers import reverse
# TODO: Reverse will change to django.urls >= 1.10
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from django.contrib.auth.models import User
from decimal import Decimal
from pdb import set_trace

class InventoryTests(APITestCase):

    def _create_product(self, title, default_price):
        """
        POST a new product and return the ID on success
        """
        url = reverse('api:product-list')
        data = {'title':title,'default_price':default_price}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data_id = response.data.get('id')
        product = Product.objects.get(id=response_data_id)
        self.assertEqual(product.title, data['title'])
        self.assertEqual(product.default_price, Decimal(data['default_price']))
        return response_data_id

    def test_create_then_update_inventory(self):
        """

        """
        data = {"title":"Test #1", "default_price":"1.11"}
        product_1 = self._create_product(**data)


        data = {'title':'Test Product #2','default_price':'2.22'}
        product_2 = self._create_product(**data)

        url = reverse('api:inventory-list')
        data = {'title': 'TEst','quantities':[{'product':product_1,'quantity':10},{'product':product_2,'quantity':20}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Inventory.objects.count(), 1)
        inv = Inventory.objects.get()
        self.assertEqual(inv.title, 'TEst')

        # Check PQs
        pq = ProductQuantity.objects.get(product=product_1,inventory=inv)
        self.assertEqual(pq.quantity, 10)
        pq = ProductQuantity.objects.get(product=product_2,inventory=inv)
        self.assertEqual(pq.quantity, 20)

        # Change PQs by using PUT to replace the inventory object
        url = reverse('api:inventory-detail',kwargs={"pk":inv.id})
        data = {'title': 'TEstUpdate','quantities':[{'product':product_1,'quantity':101},{'product':product_2,'quantity':202}]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,"{0}".format(response.status_code))
        self.assertEqual(Inventory.objects.count(), 1)
        inv = Inventory.objects.get()
        self.assertEqual(inv.title, data["title"])

        # Check PQs
        # set_trace()
        pq = ProductQuantity.objects.get(product=product_1,inventory=inv)
        self.assertEqual(pq.quantity, 101)
        pq = ProductQuantity.objects.get(product=product_2,inventory=inv)
        self.assertEqual(pq.quantity, 202)

        # Remove a quantity using PUT
        # TODO: Handle removing PQs / settign to 0 also...
        url = reverse('api:inventory-detail',kwargs={"pk":inv.id})
        data = {'title': 'TEstUpdate2','quantities':[{'product':product_2,'quantity':123}]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,"{0}".format(response.status_code))
        self.assertEqual(Inventory.objects.count(), 1)
        inv = Inventory.objects.get()
        self.assertEqual(inv.title, data["title"])

        # Check PQs
        # We Expect PQ P1 to be 0 but NOT GONE, once it is there it remains there unless deleted from PQ
        # If we don't POST a 0, it won't be removed
        pq = ProductQuantity.objects.filter(product=product_1,inventory=inv)
        self.assertEqual(pq.count(), 0)
        pq = ProductQuantity.objects.get(product=product_2,inventory=inv)
        self.assertEqual(pq.quantity, 123)
