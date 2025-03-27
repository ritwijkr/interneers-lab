import mongoengine as me
from django.db import models
from django.utils.timezone import now  
from .CategoryModel import ProductCategory

class Product(me.Document):
    name = me.StringField(max_length=255)
    description = me.StringField(blank=True, null=True)
    category = me.ReferenceField(ProductCategory, required=True, reverse_delete_rule=me.CASCADE)
    price = me.FloatField(max_digits=10, decimal_places=2)
    brand = me.StringField(max_length=100, required=True)
    quantity = me.FloatField(default=0)
    created_at = me.DateTimeField(default=now)
    updated_at = me.DateTimeField(auto_now=True)
    meta = {'collection': 'products'}

    def save(self, *args, **kwargs):
        self.updated_at = now()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
