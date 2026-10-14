from django.shortcuts import render
from .models import Usuario

# Create your views here.

def usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': usuarios})

def tarea(request):
    return render(request, 'tarea.html')

def proyecto(request):
    return render(request, 'proyecto.html')

def etiqueta(request):
    return render(request, 'etiqueta.html')

def asignacionTarea(request):
    return render(request, 'asignacionTarea.html')

def comentario(request):
    return render(request, 'comentadio.html')