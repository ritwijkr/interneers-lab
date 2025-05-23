from django.urls import path
from .views.ProductViews import ProductListView, ProductCreateView, ProductDetailView, ProductsByCategoryView
from .views.CategoryViews import CategoryListView, CategoryCreateView, ProductsByCategoryView, AddProductToCategoryView
from .web_views import product_list_view

urlpatterns = [
    path('', product_list_view, name='product-list-view'),
    # Product Routes
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<str:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/<str:category_title>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),

    # Category Routes
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<str:title>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),
    path('categories/add-product/', AddProductToCategoryView.as_view(), name='add-product-to-category'),
]
