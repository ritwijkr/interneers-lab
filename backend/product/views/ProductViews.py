from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.ProductService import ProductService

class ProductListView(APIView):
    """API endpoint to list all products."""
    def get(self, request):
        products = ProductService.list_products()
        data = [{"id": str(p.id), "name": p.name, "brand": p.brand, "category": p.category.title, "price": p.price, "quantity": p.quantity} for p in products]
        return Response(data, status=status.HTTP_200_OK)

class ProductCreateView(APIView):
    """API endpoint to create a product."""
    def post(self, request):
        name = request.data.get("name")
        description = request.data.get("description", "")
        category_title = request.data.get("category_title")
        price = request.data.get("price")
        brand = request.data.get("brand")
        quantity = request.data.get("quantity", 0)
        
        if not all([name, category_title, price, brand]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = ProductService.create_product(name, description, category_title, price, brand, quantity)
            return Response({"message": "Product created successfully", "data": {"id": str(product.id), "name": product.name}}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    """API endpoint to retrieve, update, or delete a product."""
    def get(self, request, product_id):
        product = ProductService.get_product(product_id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        data = {"id": str(product.id), "name": product.name, "brand": product.brand, "category": product.category.title, "price": product.price, "quantity": product.quantity}
        return Response(data)

    def put(self, request, product_id):
        try:
            updated_product = ProductService.update_product(product_id, **request.data)
            return Response({"message": "Product updated successfully", "product": updated_product.name})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            ProductService.delete_product(product_id)
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductsByCategoryView(APIView):
    """API endpoint to fetch products by category."""
    def get(self, request, category_title):
        try:
            products = ProductService.get_products_by_category(category_title)
            data = [{"id": str(p.id), "name": p.name, "brand": p.brand, "price": p.price} for p in products]
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
