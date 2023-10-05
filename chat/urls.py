from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.createItem, name='create'),
    path('<int:pk>/detail/', views.detail, name='detail'),
    path('<int:pk>/update/', views.updateItem, name='update'),
    path('<int:pk>/delete/', views.deleteItem, name='delete'),
    path('message/<int:pk>/', views.newMessage, name='message'),
]