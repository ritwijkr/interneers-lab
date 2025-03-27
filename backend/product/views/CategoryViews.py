from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.ProductCategoryService import ProductCategoryService

class CategoryListView(APIView):
    def get(self, request):
        categories = ProductCategoryService.list_categories()
        data = [{"id": str(cat.id), "title": cat.title, "description": cat.description} for cat in categories]
        return Response(data, status=status.HTTP_200_OK)

class CategoryCreateView(APIView):
    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description", "")
        try:
            category = ProductCategoryService.create_category(title, description)
            return Response({"message": "Category created successfully", "data": {"id": str(category.id), "title": category.title}}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductsByCategoryView(APIView):
    def get(self, request, title):
        try:
            products = ProductCategoryService.get_products_by_category(title)
            data = [{"id": str(p.id), "name": p.name, "brand": p.brand} for p in products]
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

class AddProductToCategoryView(APIView):
    def post(self, request):
        product_id = request.data.get("product_id")
        category_title = request.data.get("category_title")
        try:
            product = ProductCategoryService.add_product_to_category(product_id, category_title)
            return Response({"message": "Product added to category", "product": product.name}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
