from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
    page_size = 2  
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
