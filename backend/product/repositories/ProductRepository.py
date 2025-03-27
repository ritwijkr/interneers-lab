from ..models.ProductModel import Product
from ..models.CategoryModel import ProductCategory

class ProductRepository:
    @staticmethod
    def create(name, description, category_title, price, brand, quantity=0):
        category = ProductCategory.objects.filter(title=category_title).first()
        if not category:
            raise ValueError("Category not found.")
        product = Product(
            name=name,
            description=description,
            category=category,
            price=price,
            brand=brand,
            quantity=quantity
        )
        product.save()
        return product

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def get_all():
        return Product.objects.all()

    @staticmethod
    def get_products_by_category(category_title):
        category = ProductCategory.objects.filter(title=category_title).first()
        if not category:
            raise ValueError("Category not found.")
        return Product.objects.filter(category=category)

    @staticmethod
    def update(product_id, name=None, description=None, category_title=None, price=None, brand=None, quantity=None):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product not found.")

        if name:
            product.name = name
        if description:
            product.description = description
        if category_title:
            category = ProductCategory.objects.filter(title=category_title).first()
            if not category:
                raise ValueError("Category not found.")
            product.category = category
        if price is not None:
            product.price = price
        if brand:
            product.brand = brand
        if quantity is not None:
            product.quantity = quantity
        
        product.save()
        return product

    @staticmethod
    def delete(product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product not found.")
        product.delete()
        return True
