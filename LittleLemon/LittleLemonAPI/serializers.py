from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group
import bleach
from .models import CustomUser, Category, MenuItem, Order, OrderItem, Cart


# user model serializer
class UserSerializer(serializers.ModelSerializer):
    tel = serializers.DateField(source="contact")

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "tel",
        ]

    # Here we are going to sanitize users inputs for security reason
    def validate(self, attrs):
        attrs["first_name"] = bleach.clean(attrs["first_name"])
        attrs["last_name"] = bleach.clean(attrs["last_name"])
        attrs["username"] = bleach.clean(attrs["username"])
        attrs["contact"] = bleach.clean(attrs["contact"])
        # attrs["bio"] = bleach.clean(attrs["bio"])
        # attrs["location"] = bleach.clean(attrs["location"])
        return super().validate(attrs)


# Category serialization
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "category_title"]
        extra_kwargs = {
            "category_title": {
                "validators": [
                    UniqueValidator(queryset=Category.objects.all()),
                ],
            },
        }


# menu items serialization
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Category.objects.all(), view_name="category-detail"
    # )
    # category = serializers.HyperlinkedRelatedField(
    #     view_name="category-detail", read_only=True
    # )
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "menu_item_title",
            "price",
            "featured",
            "category",
            "category_id",
        ]
        extra_kwargs = {
            "price": {"min_value": 0.0},  # price cannot be less than 0
            "menu_item_title": {
                "validators": [
                    UniqueValidator(queryset=MenuItem.objects.all()),
                ],
            },
        }

    # checking the price, if the price is less than 0 raise a validation error

    def validate_price(self, value):
        if value < 0.0:
            ValidationError("The price cannot be less than 0")
        return value


# Cart serialization
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    # price = serializers.SerializerMethodField(method_name="calculate_total_price")

    class Meta:
        model = Cart
        fields = [
            "menuitem",
            "quantity",
            "unit_price",
            "price",
            "user",
            "user_id",
            "menuitem_id",
        ]

    # def calculate_total_price(self, cart: Cart):
    #     return cart.unit_price * cart.quantity


# order serialization


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    # validation of quantity field
    def validate_quantity(self, quantity):
        if quantity < 0:
            ValidationError("Quantity cannot be zero (0)")
        return quantity


# OrderItem serializer
class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    menuitem = MenuItemSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


# Group serializer
class GroupSerializer(serializers.ModelSerializer):
    """Group serializer"""

    class Meta:
        model = Group
        fields = "__all__"
