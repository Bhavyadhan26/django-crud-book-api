from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.get_books),
    path('books/<int:id>/', views.get_book),
    path('books/create/', views.create_book),
    path('books/update/<int:id>/', views.update_book),
    path('books/delete/<int:id>/', views.delete_book),
]