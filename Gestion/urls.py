from django.urls import path
from . import views

urlpatterns = [
    path('usuario/', views.usuario, name='usuario'),
    path('tarea/', views.usuario, name='tarea'),
    path('proyecto/', views.usuario, name='proyecto'),
    path('etiqueta/', views.usuario, name='etiqueta'),
    path('asignacionTarea/', views.usuario, name='asignacionTarea'),
    path('comentario/', views.usuario, name='comentario'),
]