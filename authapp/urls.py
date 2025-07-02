from django.urls import path 
from authapp import views

urlpatterns = [
    path('user_creation_view/', views.user_creation_view),
    path('user_authentication_view/', views.user_authentication_view),
    path('user_filter/', views.user_filter),

]