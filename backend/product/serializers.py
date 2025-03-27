from rest_framework import serializers
from .models.ProductModel import Product
from .models.CategoryModel import ProductCategory
from bson import ObjectId


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB uses string ObjectId
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    category = serializers.ListField(child=serializers.CharField())  # Expecting a list of category IDs
    price = serializers.FloatField()
    brand = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product name cannot be empty.")
        return value

    def validate_description(self, value):
        if value and not value.strip():
            raise serializers.ValidationError("Product description cannot be empty.")
        return value

    def validate_brand(self, value):
        if not value.strip():
            raise serializers.ValidationError("Brand cannot be empty.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be greater than or equal to zero.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity must be greater than or equal to zero.")
        return value

    def validate_category(self, value):
        """
        Validates category field to ensure it contains valid MongoDB ObjectIds
        and that referenced categories exist in the database.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Category must be a list of category IDs.")

        try:
            category_ids = [ObjectId(cid) for cid in value]  # Convert to ObjectId
        except Exception:
            raise serializers.ValidationError("Invalid category ID format.")

        # Fetch existing categories
        existing_categories = ProductCategory.objects(id__in=category_ids)
        existing_category_ids = {str(cat.id) for cat in existing_categories}
        
        # Identify invalid category IDs
        invalid_categories = [cid for cid in value if cid not in existing_category_ids]
        
        if invalid_categories:
            raise serializers.ValidationError(f"Invalid category IDs: {invalid_categories}")

        return existing_categories  # Return valid category instances

    def create(self, validated_data):
        """
        Handles product creation with categories as reference fields.
        """
        categories = validated_data.pop("category", [])  # Extract categories
        product = Product(category=categories, **validated_data)
        product.save()
        return product

    def update(self, instance, validated_data):
        """
        Handles product updates with proper category validation.
        """
        for key, value in validated_data.items():
            if key == "category":
                if not isinstance(value, list):
                    raise serializers.ValidationError("Category must be a list of ObjectIds.")

                try:
                    category_ids = [ObjectId(cid) for cid in value]
                except Exception:
                    raise serializers.ValidationError("Invalid category ID format.")

                categories = ProductCategory.objects(id__in=category_ids)
                if len(categories) != len(category_ids):
                    raise serializers.ValidationError("Some categories are invalid.")

                instance.category = list(categories)
            else:
                setattr(instance, key, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Converts MongoDB objects into a more readable JSON format.
        """
        return {
            "id": str(instance.id),
            "name": instance.name,
            "description": instance.description,
            "brand": instance.brand,
            "category": [cat.title for cat in instance.category if isinstance(cat, ProductCategory)],
            "price": float(instance.price),
            "quantity": int(instance.quantity),
        }
