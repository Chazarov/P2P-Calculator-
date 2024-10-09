from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('calculator', views.calculator),
    path('api/get_grid/', views.submit_parametrs)
]
