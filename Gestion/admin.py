
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Usuario,
    Proyecto,
    Tarea,
    Etiqueta,
    AsignacionTarea,
    ColaboracionProyecto,
    Comentario,
)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "username",
        "nombre",
        "email",
        "fecha_registro",
        "is_staff",
    )
    search_fields = ("username", "nombre", "email")
    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": ("nombre", "fecha_registro"),
        }),
    )


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "creador",
        "fecha_inicio",
        "fecha_finalizacion",
    )
    search_fields = ("nombre",)
    list_filter = ("fecha_inicio",)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "creador",
        "proyecto",
        "prioridad",
        "estado",
        "completada",
    )
    list_filter = ("estado", "completada", "prioridad")
    search_fields = ("titulo", "descripcion")


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(AsignacionTarea)
class AsignacionTareaAdmin(admin.ModelAdmin):
    list_display = ("tarea", "usuario", "fecha_asignacion")
    search_fields = ("tarea__titulo", "usuario__username")


@admin.register(ColaboracionProyecto)
class ColaboracionProyectoAdmin(admin.ModelAdmin):
    list_display = ("proyecto", "usuario")
    search_fields = ("proyecto__nombre", "usuario__username")


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("contenido", "autor", "tarea", "fecha_comentario")
    search_fields = ("contenido", "autor__username", "tarea__titulo")