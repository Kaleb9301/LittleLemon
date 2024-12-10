from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.menu_items, name='menu-items'),
    path('menu-items/<int:pk>', views.single_item),
    path('category/', views.category_all),
    path('category/<int:pk>', views.category_detail, name='catagory-detail'),
    path('menu', views.menu),
    path('welcome', views.welcome)
]