
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    proyectos_asignados = models.ManyToManyField(
        "Proyecto",
        through="ColaboracionProyecto",
        related_name="colaboradores",
        blank=True,
    )

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    duracion_estimada = models.FloatField()
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()

    creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="proyectos_creados",
    )

    def __str__(self):
        return self.nombre


class Tarea(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = "Pendiente", "Pendiente"
        PROGRESO = "Progreso", "Progreso"
        COMPLETADA = "Completada", "Completada"

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.IntegerField()

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    hora_vencimiento = models.TimeField()

    creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="tareas_creadas",
    )

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="tareas",
    )

    usuarios_asignados = models.ManyToManyField(
        Usuario,
        through="AsignacionTarea",
        related_name="tareas_asignadas",
        blank=True,
    )

    etiquetas = models.ManyToManyField(
        "Etiqueta",
        related_name="tareas",
        blank=True,
    )

    def __str__(self):
        return self.titulo


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class AsignacionTarea(models.Model):
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name="asignaciones",
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="asignaciones_tareas",
    )

    observaciones = models.TextField()
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tarea", "usuario"],
                name="unique_asignacion_tarea_usuario",
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.tarea}"


class ColaboracionProyecto(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="colaboraciones_proyecto",
    )

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="colaboraciones",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "proyecto"],
                name="unique_colaboracion_usuario_proyecto",
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.proyecto}"


class Comentario(models.Model):
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )

    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )

    def __str__(self):
        return f"Comentario de {self.autor} en {self.tarea}"