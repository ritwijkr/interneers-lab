from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .services import ProductService
from .serializers import ProductSerializer

# Pagination for Product List API
class ProductPagination(PageNumberPagination):
    page_size = 2  
    page_size_query_param = 'page_size'  
    max_page_size = 100


class ProductCreate(generics.CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = ProductService.create_product(serializer.validated_data)
            return Response({"message": "Product created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# List Products API
class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return ProductService.list_products()

# Product Detail API
class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "id"

    def get(self, request, id, *args, **kwargs):
        product = ProductService.get_product(id)
        if not product:
            raise NotFound({"error": "Product not found"})
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Update Product API
class ProductUpdate(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    lookup_field = "id"

    def update(self, request, id, *args, **kwargs):
        product = ProductService.update_product(id, request.data)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(product)
        return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

# Delete Product API
class ProductDelete(generics.DestroyAPIView):
    lookup_field = "id"

    def delete(self, request, id, *args, **kwargs):
        success = ProductService.delete_product(id)
        if success:
            return Response({"message": "Successfully deleted"}, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)