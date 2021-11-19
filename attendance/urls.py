from django.urls import path
from . import views

urlpatterns = [
    path('attendance/book_register/', views.register, name='book_register'),
    path('attendance/book_register/save', views.register_save, name='book_register_save'),
    path('attendance/book/', views.book, name='book'),
    path('attendance/book/save', views.book_save, name='book_save'),
    path('attendance/book/search', views.book_search, name='book_search'),
    path('attendance/book/search/pdf_view', views.ViewPDF.as_view(), name='book_search_pdf'),
]