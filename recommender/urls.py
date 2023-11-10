# urls.py
from django.urls import path

from .views import index_view, recommend_view

urlpatterns = [
    path('', index_view, name='index'),
    path('recommend', recommend_view, name='recommend'),
]
