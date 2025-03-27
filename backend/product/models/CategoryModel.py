import mongoengine as me
from django.utils.timezone import now  

class ProductCategory(me.Document):
    title = me.StringField(max_length=100, required=True, unique=True)
    description = me.StringField()
    created_at = me.DateTimeField(default=now)
    updated_at = me.DateTimeField(default=now)

    meta = {'collection': 'product_categories'}

    def save(self, *args, **kwargs):
        self.updated_at = now()
        return super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
