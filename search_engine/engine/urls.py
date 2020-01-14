from django.urls import path
from engine import views

urlpatterns = [
    path('search/',views.search,name='search'),
]
