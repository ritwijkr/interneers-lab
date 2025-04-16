import unittest
from unittest.mock import patch, MagicMock
from product.repositories.CategoryRepository import CategoryRepository

class TestCategoryRepository(unittest.TestCase):

    @patch("product.repositories.CategoryRepository.ProductCategory")
    def test_create_category_success(self, mock_product_category):
        mock_objects = MagicMock()
        mock_objects.filter.return_value.first.return_value = None
        mock_product_category.objects = mock_objects

        mock_category_instance = MagicMock()
        mock_product_category.return_value = mock_category_instance

        result = CategoryRepository.create("Electronics", "All electronic items")

        mock_product_category.objects.filter.assert_called_once_with(title="Electronics")
        mock_product_category.assert_called_once_with(title="Electronics", description="All electronic items")
        mock_category_instance.save.assert_called_once()
        self.assertEqual(result, mock_category_instance)

    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_create_category_already_exists(self, mock_category_objects):
        mock_category_objects.filter.return_value.first.return_value = MagicMock()

        with self.assertRaises(ValueError) as context:
            CategoryRepository.create("Electronics", "Some description")
        self.assertEqual(str(context.exception), "Category with this title already exists.")

    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_get_category_by_title(self, mock_category_objects):
        mock_category = MagicMock()
        mock_category_objects.filter.return_value.first.return_value = mock_category

        result = CategoryRepository.get_category_by_title("Electronics")
        self.assertEqual(result, mock_category)
        mock_category_objects.filter.assert_called_once_with(title="Electronics")

    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_get_all_categories(self, mock_category_objects):
        mock_categories = [MagicMock(), MagicMock()]
        mock_category_objects.all.return_value = mock_categories

        result = CategoryRepository.get_all()
        self.assertEqual(result, mock_categories)
        mock_category_objects.all.assert_called_once()

    @patch("product.models.ProductModel.Product.objects")
    def test_get_products_by_category(self, mock_product_objects):
        mock_products = [MagicMock(), MagicMock()]
        mock_product_objects.filter.return_value = mock_products

        category = MagicMock()
        result = CategoryRepository.get_products_by_category(category)
        self.assertEqual(result, mock_products)
        mock_product_objects.filter.assert_called_once_with(category=category)

    @patch("product.models.ProductModel.Product.objects")
    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_add_product_to_category_success(self, mock_category_objects, mock_product_objects):
        mock_category = MagicMock()
        mock_product = MagicMock()
        mock_category_objects.filter.return_value.first.return_value = mock_category
        mock_product_objects.filter.return_value.first.return_value = mock_product

        result = CategoryRepository.add_product_to_category("123", "Electronics")
        self.assertEqual(result, mock_product)
        self.assertEqual(mock_product.category, mock_category)
        mock_product.save.assert_called_once()

    @patch("product.models.ProductModel.Product.objects")
    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_add_product_to_category_failure(self, mock_category_objects, mock_product_objects):
        mock_category_objects.filter.return_value.first.return_value = None
        mock_product_objects.filter.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            CategoryRepository.add_product_to_category("123", "Electronics")
        self.assertEqual(str(context.exception), "Invalid product or category.")

    @patch("product.models.ProductModel.Product.objects")
    def test_remove_product_from_category_success(self, mock_product_objects):
        mock_product = MagicMock()
        mock_product_objects.filter.return_value.first.return_value = mock_product

        result = CategoryRepository.remove_product_from_category("123")
        self.assertIsNone(mock_product.category)
        mock_product.save.assert_called_once()
        self.assertEqual(result, mock_product)

    @patch("product.models.ProductModel.Product.objects")
    def test_remove_product_from_category_failure(self, mock_product_objects):
        mock_product_objects.filter.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            CategoryRepository.remove_product_from_category("123")
        self.assertEqual(str(context.exception), "Product not found.")

    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_update_category_success(self, mock_category_objects):
        mock_category = MagicMock()
        mock_category_objects.filter.side_effect = [
            MagicMock(first=MagicMock(return_value=mock_category)),  # Existing category
            MagicMock(first=MagicMock(return_value=None))            # No conflict with new title
        ]

        result = CategoryRepository.update("Electronics", new_title="Gadgets", new_description="All gadgets")
        self.assertEqual(result, mock_category)
        self.assertEqual(mock_category.title, "Gadgets")
        self.assertEqual(mock_category.description, "All gadgets")
        mock_category.save.assert_called_once()

    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_update_category_not_found(self, mock_category_objects):
        mock_category_objects.filter.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            CategoryRepository.update("NonExisting", new_title="NewTitle")
        self.assertEqual(str(context.exception), "Category not found.")

    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_update_category_duplicate_title(self, mock_category_objects):
        mock_category = MagicMock()
        mock_category_objects.filter.side_effect = [
            MagicMock(first=MagicMock(return_value=mock_category)),  # existing category
            MagicMock(first=MagicMock(return_value=MagicMock()))     # new title exists
        ]

        with self.assertRaises(ValueError) as context:
            CategoryRepository.update("Electronics", new_title="Duplicate")
        self.assertEqual(str(context.exception), "Category with this new title already exists.")

    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_delete_category_success(self, mock_category_objects):
        mock_category = MagicMock()
        mock_category_objects.filter.return_value.first.return_value = mock_category

        result = CategoryRepository.delete("Electronics")
        mock_category.delete.assert_called_once()
        self.assertTrue(result)

    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_delete_category_not_found(self, mock_category_objects):
        mock_category_objects.filter.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            CategoryRepository.delete("NonExisting")
        self.assertEqual(str(context.exception), "Category not found.")

if __name__ == '__main__':
    unittest.main()
