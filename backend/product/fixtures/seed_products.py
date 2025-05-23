from mongoengine import connect
from product.models.ProductModel import Product
from product.models.CategoryModel import ProductCategory

connect("test_db", host="mongodb://localhost:27017/")

def run():
    Product.objects.delete()
    ProductCategory.objects.delete()

    electronics = ProductCategory(title="Electronics").save()
    kitchen = ProductCategory(title="Kitchen Essentials").save()

    Product(
        name="Smartphone",
        description="Latest model",
        category=electronics,
        price=999.99,
        brand="BrandX",
        quantity=50,
    ).save()

    Product(
        name="Mixer",
        description="500W mixer",
        category=kitchen,
        price=199.99,
        brand="KitchenPro",
        quantity=20,
    ).save()

    print("Seed data insertion successful")

if __name__ == "__main__":
    run()
