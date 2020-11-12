
from .views import register
from django.urls import path,include
from. import views

urlpatterns = [
    path('register/', register, name='register'),
    path('', views.UserListView.as_view(),name='home-user'),
    path('update/<pk>', views.UserUpdateView.as_view(),name='update-user')
]