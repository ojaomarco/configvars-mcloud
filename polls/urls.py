from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('processaformulario/', views.processa_formulario, name="processa_formulario")
]
