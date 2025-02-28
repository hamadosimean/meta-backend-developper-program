from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("menu-items", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.MenuItemDetailView.as_view()),
    path(
        "category-detail/<int:pk>",
        views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path("auth-token-obtain/", obtain_auth_token),
]
