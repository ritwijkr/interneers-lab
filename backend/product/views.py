from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError
from .models import Product
from .serializers import ProductSerializer

# Pagination for Product List API
class ProductPagination(PageNumberPagination):
    """
    Custom pagination class for handling product list pagination.
    - page_size: Defines the default number of products per page (2 in this case).
    - page_size_query_param: Allows the client to request a different page size via query params.
    - max_page_size: Restricts the maximum number of products per page (100) to prevent overloading the API.
    """
    page_size = 10  
    page_size_query_param = 'page_size'  
    max_page_size = 100  

# Create a Product
class ProductCreate(generics.CreateAPIView):
    """
    API endpoint to create a new product.
    - Uses `CreateAPIView`, which provides the default implementation of POST requests.
    - Automatically validates data and saves a new product instance.
    - Returns a 201 Created response on success.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def create(self, request, *args, **kwargs):
        """Handles product creation with validation error handling."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

# Fetch List of Products (with Pagination)
class ProductList(generics.ListAPIView):
    """
    API endpoint to retrieve a paginated list of products.
    - Uses `ListAPIView`, which provides the default implementation for GET requests.
    - Implements pagination using the `ProductPagination` class.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    def list(self, request, *args, **kwargs):
        """Fetches all products with proper error handling if no products exist."""
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)
        return super().list(request, *args, **kwargs)


# Fetch a Single Product
class ProductDetail(generics.RetrieveAPIView):
    """
    API endpoint to retrieve details of a single product.
    - Uses `RetrieveAPIView`, which handles GET requests for a single object.
    - Looks up a product by its `id` field.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    def get_object(self):
        """Fetches a product by ID and raises a custom error if not found."""
        try:
            return super().get_object()
        except Product.DoesNotExist:
            raise NotFound({"error": "Product not found with the given ID."})

# Update a Product
class ProductUpdate(generics.UpdateAPIView):
    """
    API endpoint to update an existing product.
    - Uses `UpdateAPIView`, which provides default handling for PUT & PATCH requests.
    - Looks up the product using its `id` and updates the relevant fields.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    def update(self, request, *args, **kwargs):
        """Handles product updates with validation error handling."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Delete a Product
class ProductDelete(generics.DestroyAPIView):
    """
    API endpoint to delete an existing product.
    - Uses `DestroyAPIView`, which provides default handling for DELETE requests.
    - Deletes the product identified by its `id`.
    - Returns a 204 No Content response on success.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    def delete(self, request, *args, **kwargs):
        """Deletes a product with appropriate error handling."""
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response({"message": "Successfully deleted"}, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
