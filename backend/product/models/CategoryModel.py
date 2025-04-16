import mongoengine as me
from mongoengine import Document, StringField, DateTimeField
import datetime


class ProductCategory(me.Document):
    title = me.StringField(max_length=100, required=True, unique=True)
    description = me.StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    meta = {'collection': 'product_categories'}

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
