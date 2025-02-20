from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import bleach
from .models import CustomUser, Category, MenuItem, Order, OrderItem, Cart


# user model serializer
class UserSerializer(serializers.ModelSerializer):
    date_birth = serializers.DateField(source="birth_date")

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "contact",
            "bio",
            "location",
            "photo",
            "date_birth",
        ]

    # Here we are going to sanitize users inputs for security reason
    def validate(self, attrs):
        attrs["first_name"] = bleach.clean(attrs["first_name"])
        attrs["last_name"] = bleach.clean(attrs["last_name"])
        attrs["username"] = bleach.clean(attrs["username"])
        attrs["contact"] = bleach.clean(attrs["contact"])
        attrs["bio"] = bleach.clean(attrs["bio"])
        attrs["location"] = bleach.clean(attrs["location"])
        return super().validate(attrs)


# Category serialization
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title"]


# menu items serialization
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "featured", "image", "category"]
        extra_kwargs = {"price": {"min_value": 0}}

    # checking the price, if the price is less than 0 raise a validation error

    def validate_price(self, value):
        if value < 0.0:
            ValidationError("The price cannot be less than 0")
        return value


# Cart serialization
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menuitem = MenuItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="calcuate_total_price")

    class Meta:
        model = Cart
        fields = ["menuitem", "quantity", "unit_price", "total_price", "user"]

    def calcuate_total_price(slef, cart: Cart):
        return cart.price * cart.quantity


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
    user = UserSerializer(read_only=True)
    menuitem = MenuItemSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = "__all__"
