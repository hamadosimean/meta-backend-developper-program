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
    GroupSerializer,
    CustomUser,
)
from .permissions import IsManagerOrReadOnly, OnlyManager


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


class MenuItemDetailView(APIView):
    """Retreive , update or delete Menu Item"""

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


# Manager management


class ManagerView(APIView):
    """Manager view handling manager related logiic"""

    permission_classes = [OnlyManager]

    def get(self, request):
        """return all managers"""
        managers = Group.objects.filter(name="Manager")
        serializer = GroupSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Asign an user to a group"""
        username = request.data.get("username")
        if username:
            if CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.get(username=username)
                manager = Group.objects.get(name="Manager")
                manager.user_set.add(user)
                return Response(
                    {"message": f"{username} is assign to {manager.name} goup"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"Message": f"{username} is not yet registered"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


# Manager detail view
class ManagerDetailView(APIView):
    """Manage individual user"""

    permission_classes = [OnlyManager]  # only manager can perform following actions

    def delete(self, request, userId):
        """delete a particular user from a group"""
        user = get_object_or_404(CustomUser, pk=userId)
        if user:
            group = Group.objects.get(user=user, name="Manager")
            if group:
                group.user_set.remove(user)
                return Response(
                    {"message": f"{user.username} has been deleted from {group.name}"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": f"{user.username} was not assigned to {group.name}"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"message": f"cannot found"},
                status=status.HTTP_404_NOT_FOUND,
            )


# Delivery crew management


class DeliveryCrewManagementView(APIView):
    permission_classes = [OnlyManager]

    def get(self, request):
        """return all delivery crew"""
        delivery_crew = Group.objects.filter(name="Delivery crew")
        serializer = GroupSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Asign an user to a delivery crew group"""
        username = request.POST.get("username")
        if username:
            if CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.get(username=username)
                delivery_crew = Group.objects.get(name="Delivery crew")
                delivery_crew.user_set.add(user)
                return Response(
                    {"message": f"{username} is assign to {delivery_crew.name} goup"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"Message": f"{username} is not yet registered"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class DeliveryCrewDetailView(APIView):
    """Manage individual user"""

    permission_classes = [OnlyManager]  # only manager can perform following actions

    def delete(self, request, userId):
        """delete a particular user from a group"""

        if CustomUser.objects.filter(pk=userId).exists():
            user = get_object_or_404(CustomUser, pk=userId)
            if Group.objects.filter(user=user).exists():
                group = Group.objects.get(user=user, name="Delivery crew")
                group.user_set.remove(user)
                return Response(
                    {"message": f"{user.username} has been deleted from {group.name}"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": f"{user.username} was not assigned to delivery crew"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"message": "Cannot found"},
                status=status.HTTP_404_NOT_FOUND,
            )
