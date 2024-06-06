from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name="main"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('description', views.product_description, name="product_description")
    # path('register/', views.register_view, name="register")
]