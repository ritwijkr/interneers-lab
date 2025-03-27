from django.urls import path
from .views.views import ProductCreate, ProductList, ProductDetail, ProductUpdate, ProductDelete
from .views.CategoryViews import CategoryListView, CategoryCreateView, ProductsByCategoryView, AddProductToCategoryView

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/create/', ProductCreate.as_view(), name='product-create'),
    path('products/<str:id>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<str:id>/update/', ProductUpdate.as_view(), name='product-update'),
    path('products/<str:id>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<str:title>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),
    path('categories/add-product/', AddProductToCategoryView.as_view(), name='add-product-to-category'),

]
