from django.db import models

# Create your models here.
class Inventory(models.Model):
    # Optional title, else Inventory
    title = models.CharField(default="Inventory",max_length=64)

class Product(models.Model):
    # ProductPrice overrides this
    default_price = models.DecimalField(decimal_places=2, max_digits=10, default="50.00")

    # Short title for the product
    title = models.CharField(null=False,blank=False,max_length=64)

    # Long, internal description
    # etc

class ProductQuantity(models.Model):
    product=models.ForeignKey("Product",related_name="+",null=False,blank=False)
    inventory=models.ForeignKey("Inventory",related_name="quantities",null=False,blank=False)
    quantity=models.PositiveIntegerField(default=0)
