from ..repositories.CategoryRepository import CategoryRepository

class ProductCategoryService:
    @staticmethod
    def create_category(title, description=None):
        return CategoryRepository.create(title, description)

    @staticmethod
    def get_category(title):
        return CategoryRepository.get_category_by_title(title)

    @staticmethod
    def list_categories():
        return CategoryRepository.get_all()

    @staticmethod
    def get_products_by_category(title):
        category = CategoryRepository.get_category_by_title(title)
        if not category:
            raise ValueError("Category not found.")
        return CategoryRepository.get_products_by_category(category)

    @staticmethod
    def add_product_to_category(product_id, category_title):
        return CategoryRepository.add_product_to_category(product_id, category_title)

    @staticmethod
    def remove_product_from_category(product_id):
        return CategoryRepository.remove_product_from_category(product_id)

    @staticmethod
    def update_category(title, new_title=None, new_description=None):
        return CategoryRepository.update(title, new_title, new_description)

    @staticmethod
    def delete_category(title):
        return CategoryRepository.delete(title)
