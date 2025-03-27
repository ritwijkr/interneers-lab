from product.models.ProductModel import Product
from product.models.CategoryModel import ProductCategory

category = ProductCategory.objects.filter(title="Electronics").first()
if category:
    products = Product.objects.filter(category=category)
    print(products)
else:
    print("Category not found!")
