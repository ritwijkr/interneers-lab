import unittest
from mongoengine import connect, disconnect
from product.models.ProductModel import Product
from product.models.CategoryModel import ProductCategory
from product.services.ProductService import ProductService

class IntegrationTestProductService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect('test_db', host='localhost', port=27017)

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def setUp(self):
        Product.objects.delete()
        ProductCategory.objects.delete()

        self.category = ProductCategory(title="Electronics").save()

    def test_create_and_fetch_product(self):
        ProductService.create_product(
            name="Laptop",
            description="Gaming laptop",
            category_title="Electronics",
            price=2000,
            brand="Alienware",
            quantity=5,
        )

        products = ProductService.get_products_by_category("Electronics")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Laptop")

    def test_get_products_invalid_category(self):
        with self.assertRaises(ValueError):
            ProductService.get_products_by_category("Unknown")

