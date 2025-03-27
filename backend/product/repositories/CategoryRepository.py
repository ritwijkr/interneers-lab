from ..models.CategoryModel import ProductCategory
from ..models.ProductModel import Product

class CategoryRepository:
    @staticmethod
    def create(title, description=None):
        if ProductCategory.objects.filter(title=title).first():
            raise ValueError("Category with this title already exists.")
        category = ProductCategory(title=title, description=description)
        category.save()
        return category

    @staticmethod
    def get_category_by_title(title):
        return ProductCategory.objects.filter(title=title).first()

    @staticmethod
    def get_all():
        return ProductCategory.objects.all()

    @staticmethod
    def get_products_by_category(category):
        return Product.objects.filter(category=category)

    @staticmethod
    def add_product_to_category(product_id, category_title):
        """Assigns a product to a category."""
        category = ProductCategory.objects.filter(title=category_title).first()
        product = Product.objects.filter(id=product_id).first()
        if not category or not product:
            raise ValueError("Invalid product or category.")
        product.category = category
        product.save()
        return product

    @staticmethod
    def remove_product_from_category(product_id):
        """Removes a product from its category (sets to None)."""
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product not found.")
        product.category = None
        product.save()
        return product

    @staticmethod
    def update(title, new_title=None, new_description=None):
        category = ProductCategory.objects.filter(title=title).first()
        if not category:
            raise ValueError("Category not found.")
        if new_title and ProductCategory.objects.filter(title=new_title).first():
            raise ValueError("Category with this new title already exists.")
        if new_title:
            category.title = new_title
        if new_description is not None:
            category.description = new_description
        category.save()
        return category

    @staticmethod
    def delete(title):
        category = ProductCategory.objects.filter(title=title).first()
        if not category:
            raise ValueError("Category not found.")
        category.delete()
        return True
