from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS,
)
from django.contrib.auth.models import User, Group
from .throttles import TenCallPerMinute

# models import
from .models import Cart, Category, CustomUser, MenuItem, Order, OrderItem

# serializers import
from .serializers import (
    CartSerializer,
    MenuItemSerializer,
    OrderItemSerializer,
    OrderSerializer,
    CategorySerializer,
)
from .permission import IsManagerOrReadOnly

# defining authoriazation classes


# Create your views here.


# Function based menu items views
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def menu_items_view(request):
#     if request.method == "GET":
#         menuitems = MenuItem.objects.select_related("category").all()
#         serializer = MenuItemSerializer(menuitems, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if (
#         request.user.groups.filter(name="manager").exists() or request.user.is_superuser
#     ):  # check if user is a manager
#         if request.method == "POST":
#             serializer = MenuItemSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(
#             {"Error": "403 – Unauthorized"}, status=status.HTTP_403_FORBIDDEN
#         )


# class based view menu items


class MenuItemsView(APIView):
    """List all menu items or create new ones"""

    # customize permissions class so manager can perform CRUD on the object
    # and other users like customizer and deliveyr crew can only view
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManagerOrReadOnly]
        return super().get_permissions()

    # list all menu items
    def get(self, request, format=None):
        menuitems = MenuItem.objects.all()
        serializer = MenuItemSerializer(menuitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # add menu items
    def post(self, request, format=None):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view for category detail
class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return

    def get(self, request, pk):
        category = self.get_object(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


#  Menu details view: function base
# @permission_classes([IsAuthenticated])
# @api_view(["GET", "PUT", "PATCH"])
# def menu_detail_view(request, pk):
#     menuitem = get_object_or_404(MenuItem, pk=pk)
#     serializer = MenuItemSerializer(menuitem)
#     return Response(serializer.data, status=status.HTTP_200_OK)
class MenuItemDetailView(APIView):
    """Retreive , update or detail Menu Items"""

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManagerOrReadOnly]
        return super().get_permissions()

    # getting the object
    def get_object(self, pk):
        return get_object_or_404(MenuItem, pk=pk)

    def get(self, request, pk):
        menuitem = self.get_object(pk=pk)
        serializer = MenuItemSerializer(menuitem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        menuitem = self.get_object(pk=pk)
        serializer = MenuItemSerializer(menuitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        menuitem = self.get_object(pk=pk)
        serializer = MenuItemSerializer(menuitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menuitem = self.get_object(pk=pk)
        menuitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
