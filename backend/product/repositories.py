from .models import Product

class ProductRepository:

    @staticmethod
    def create_product(product_data):
        product = Product(**product_data)
        product.save()
        return product

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects(id=product_id).first()

    @staticmethod
    def update_product(product_id, update_data):
        product = Product.objects(id=product_id).first()
        if product:
            product.update(**update_data)
            product.reload()  # Reload to get updated data
            return product
        return None

    @staticmethod
    def delete_product(product_id):
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
            return True
        return False
