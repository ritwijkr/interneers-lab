import unittest
from unittest.mock import patch, MagicMock
from product.services.ProductService import ProductService
from mongoengine.errors import ValidationError

class TestProductService(unittest.TestCase):
    # Test case for creating a product with a brand
    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_create_product_with_brand(self, mock_category_objects):
        mock_category = MagicMock()
        mock_category_objects.filter.return_value.first.return_value = mock_category

        with patch("product.repositories.ProductRepository.Product") as mock_product_class:
            mock_product_instance = MagicMock()
            mock_product_class.return_value = mock_product_instance

            ProductService.create_product(
                name="Phone",
                description="A smart phone",
                category_title="Electronics",
                price=1000,
                brand="BrandX",
                quantity=10,
            )

            mock_product_class.assert_called_once_with(
                name="Phone",
                description="A smart phone",
                category=mock_category,
                price=1000,
                brand="BrandX",
                quantity=10,
            )
            mock_product_instance.save.assert_called_once() 

    @patch("product.models.CategoryModel.ProductCategory.objects") 
    def test_create_product_without_brand_should_fail(self, mock_category_objects):
        mock_category = MagicMock()
        mock_category_objects.filter.return_value.first.return_value = mock_category
        with patch("product.repositories.ProductRepository.Product") as mock_product_class:
            mock_product_instance = MagicMock()
            mock_product_instance.save.side_effect = ValidationError("brand is required")
            mock_product_class.return_value = mock_product_instance
            with self.assertRaises(ValidationError) as context:
                ProductService.create_product(
                    name="Phone",
                    description="A smart phone",
                    category_title="Electronics",
                    price=1000,
                    brand=None,
                    quantity=10,
                )

            self.assertIn("brand", str(context.exception))
    
    @patch("product.models.CategoryModel.ProductCategory.objects")
    def test_create_product_without_category_should_fail(self, mock_category_objects):
        mock_category_objects.filter.return_value.first.return_value = None
        with self.assertRaises(ValueError) as context:
            ProductService.create_product(
                name="Phone",
                description="A smart phone",
                category_title="non-existent category",
                price=1000,
                brand="BrandX",
                quantity=10,
            )

        self.assertEqual(str(context.exception), "Category not found.")

    @patch("product.models.ProductModel.Product.objects")
    def test_get_product_by_id(self, mock_product_objects):
        mock_product = MagicMock()
        mock_product.id = "238329"
        mock_product_objects.filter.return_value.first.return_value = mock_product

        result = ProductService.get_product("238329")
        self.assertEqual(result.id, "238329")
        mock_product_objects.filter.assert_called_once_with(id="238329")

    @patch("product.repositories.ProductRepository.Product")
    def test_list_products(self, mock_product_model):
        mock_product_1 = MagicMock()
        mock_product_2 = MagicMock()
        mock_product_model.objects.all.return_value = [mock_product_1, mock_product_2]

        products = ProductService.list_products()

        mock_product_model.objects.all.assert_called_once()
        self.assertEqual(products, [mock_product_1, mock_product_2])

    @patch("product.repositories.ProductRepository.Product")
    @patch("product.repositories.ProductRepository.ProductCategory")
    def test_get_products_by_category(self, mock_category_class, mock_product_class):
        mock_category = MagicMock()
        mock_category_class.objects.filter.return_value.first.return_value = mock_category

        mock_product_1 = MagicMock()
        mock_product_2 = MagicMock()
        mock_product_class.objects.filter.return_value = [mock_product_1, mock_product_2]

        category_title = "Electronics"
        result = ProductService.get_products_by_category(category_title)

        mock_category_class.objects.filter.assert_called_once_with(title=category_title)
        mock_product_class.objects.filter.assert_called_once_with(category=mock_category)
        self.assertEqual(result, [mock_product_1, mock_product_2])

    @patch("product.repositories.ProductRepository.ProductCategory")
    def test_get_products_by_invalid_category_should_raise_error(self, mock_category_class):
        mock_category_class.objects.filter.return_value.first.return_value = None

        category_title = "NonExistentCategory"

        with self.assertRaises(ValueError) as context:
            ProductService.get_products_by_category(category_title)

        self.assertEqual(str(context.exception), "Category not found.")
        mock_category_class.objects.filter.assert_called_once_with(title=category_title)

    @patch("product.repositories.ProductRepository.ProductCategory")
    @patch("product.repositories.ProductRepository.Product")
    def test_update_product_success(self, mock_product_model, mock_category_model):
        mock_product = MagicMock()
        mock_product_model.objects.filter.return_value.first.return_value = mock_product

        mock_category = MagicMock()
        mock_category_model.objects.filter.return_value.first.return_value = mock_category

        result = ProductService.update_product(
            product_id="123",
            name="Updated Name",
            description="Updated Description",
            category_title="Updated Category",
            price=999,
            brand="Updated Brand",
            quantity=50
        )
        self.assertEqual(result, mock_product)
        self.assertEqual(mock_product.name, "Updated Name")
        self.assertEqual(mock_product.description, "Updated Description")
        self.assertEqual(mock_product.category, mock_category)
        self.assertEqual(mock_product.price, 999)
        self.assertEqual(mock_product.brand, "Updated Brand")
        self.assertEqual(mock_product.quantity, 50)
        mock_product.save.assert_called_once()

    @patch("product.repositories.ProductRepository.Product")
    def test_update_product_not_found(self, mock_product_model):
        mock_product_model.objects.filter.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            ProductService.update_product(product_id="999")

        self.assertEqual(str(context.exception), "Product not found.")

    @patch("product.repositories.ProductRepository.ProductCategory")
    @patch("product.repositories.ProductRepository.Product")
    def test_update_product_category_not_found(self, mock_product_model, mock_category_model):
        mock_product = MagicMock()
        mock_product_model.objects.filter.return_value.first.return_value = mock_product

        mock_category_model.objects.filter.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            ProductService.update_product(product_id="123", category_title="Nonexistent Category")

        self.assertEqual(str(context.exception), "Category not found.")

    @patch("product.models.ProductModel.Product.objects")
    def test_delete_product_success(self, mock_product_objects):
        mock_product = MagicMock()
        mock_product_objects.filter.return_value.first.return_value = mock_product

        result = ProductService.delete_product("123")

        mock_product_objects.filter.assert_called_once_with(id="123")
        mock_product.delete.assert_called_once()
        self.assertTrue(result)

    @patch("product.models.ProductModel.Product.objects")
    def test_delete_product_not_found(self, mock_product_objects):
        mock_product_objects.filter.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            ProductService.delete_product("123")

        mock_product_objects.filter.assert_called_once_with(id="123")
        self.assertEqual(str(context.exception), "Product not found.")
if __name__ == "__main__":
    unittest.main()