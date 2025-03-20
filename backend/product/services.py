from .repositories import ProductRepository

class ProductService:

    @staticmethod
    def create_product(product_data):
        return ProductRepository.create_product(product_data)

    @staticmethod
    def list_products():
        return ProductRepository.get_all_products()

    @staticmethod
    def get_product(product_id):
        return ProductRepository.get_product_by_id(product_id)

    @staticmethod
    def update_product(product_id, update_data):
        return ProductRepository.update_product(product_id, update_data)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete_product(product_id)
