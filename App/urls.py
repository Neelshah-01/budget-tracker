from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_home),
    path('home/', views.home, name='home'),
    path('new_transaction/', views.new_transaction, name='new_transaction'),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('delete_transaction/<int:pk>/', views.delete_transaction, name='delete_transaction'),
]
