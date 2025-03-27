from ..repositories.ProductRepository import ProductRepository

class ProductService:
    @staticmethod
    def create_product(name, description, category_title, price, brand, quantity=0):
        return ProductRepository.create(name, description, category_title, price, brand, quantity)

    @staticmethod
    def get_product(product_id):
        return ProductRepository.get_product_by_id(product_id)

    @staticmethod
    def list_products():
        return ProductRepository.get_all()

    @staticmethod
    def get_products_by_category(category_title):
        return ProductRepository.get_products_by_category(category_title)

    @staticmethod
    def update_product(product_id, **kwargs):
        return ProductRepository.update(product_id, **kwargs)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete(product_id)
