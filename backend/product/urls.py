from django.urls import path
from .views import ProductCreate, ProductList, ProductDetail, ProductUpdate, ProductDelete

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),       # Fetch All Products
    path('products/create/', ProductCreate.as_view(), name='product-create'), # Create Product
    path('products/<int:id>/', ProductDetail.as_view(), name='product-detail'), # Fetch One Product
    path('products/<int:id>/update/', ProductUpdate.as_view(), name='product-update'), # Update Product
    path('products/<int:id>/delete/', ProductDelete.as_view(), name='product-delete'), # Delete Product
]
