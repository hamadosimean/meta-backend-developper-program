from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path(
        "menu-items", views.MenuItemsView.as_view()
    ),  # menu items list of all menu items
    path(
        "menu-items/<int:pk>", views.MenuItemDetailView.as_view()
    ),  # menu item details
    # path("category-detail/<int:pk>",views.CategoryDetailView.as_view(),name="category-detail"),
    path("groups/manager/users", views.ManagerView.as_view()),  # users management
    path(
        "groups/manager/users/<int:userId>", views.ManagerDetailView.as_view()
    ),  # manageement detail view
    path("groups/delivery-crew/users", views.DeliveryCrewManagementView.as_view()),
    path(
        "groups/delivery-crew/users/<int:userId>",
        views.DeliveryCrewDetailView.as_view(),
    ),  # delivery crew management
    path("auth-token-obtain/", obtain_auth_token),
]
