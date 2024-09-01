from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('disclaimer', views.disclaimer, name='home'),
]
