import mongoengine as me
from mongoengine import Document, StringField, DateTimeField
import datetime
from .CategoryModel import ProductCategory

class Product(me.Document):
    name = me.StringField(max_length=255, required=True)
    description = me.StringField()
    category = me.ReferenceField(ProductCategory, required=True, reverse_delete_rule=me.CASCADE)
    price = me.FloatField(required=True)
    brand = me.StringField(max_length=100, required=True)  # Enforcing brand as required
    quantity = me.IntField(default=0, min_value=0)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    meta = {'collection': 'products'}

    def save(self, *args, **kwargs):
        """Auto-update `updated_at` timestamp on save."""
        self.updated_at = datetime.datetime.now()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
