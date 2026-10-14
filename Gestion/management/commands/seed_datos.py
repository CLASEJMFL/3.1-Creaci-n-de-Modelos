
from datetime import date, time, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from Gestion.models import (
    Proyecto,
    Tarea,
    Etiqueta,
    AsignacionTarea,
    ColaboracionProyecto,
    Comentario,
)

Usuario = get_user_model()


class Command(BaseCommand):
    help = "Genera 30 registros de ejemplo por cada modelo de Gestion"

    def handle(self, *args, **options):
        hoy = date.today()

        # 1. Crear 30 usuarios
        usuarios = []

        for i in range(1, 31):
            usuario, creado = Usuario.objects.get_or_create(
                username=f"usuario{i}",
                defaults={
                    "nombre": f"Usuario {i}",
                    "email": f"usuario{i}@ejemplo.com",
                    "is_active": True,
                },
            )

            if creado:
                usuario.set_password("Prueba12345!")
                usuario.save()

            usuarios.append(usuario)

        # 2. Crear 30 proyectos
        proyectos = []

        for i in range(1, 31):
            proyecto, _ = Proyecto.objects.get_or_create(
                nombre=f"Proyecto {i}",
                defaults={
                    "descripcion": f"Descripción del proyecto {i}",
                    "duracion_estimada": float(i * 2),
                    "fecha_inicio": hoy + timedelta(days=i),
                    "fecha_finalizacion": hoy + timedelta(days=i + 30),
                    "creador": usuarios[(i - 1) % 30],
                },
            )
            proyectos.append(proyecto)

        # 3. Crear 30 etiquetas
        etiquetas = []

        for i in range(1, 31):
            etiqueta, _ = Etiqueta.objects.get_or_create(
                nombre=f"Etiqueta {i}"
            )
            etiquetas.append(etiqueta)

        # 4. Crear 30 tareas
        tareas = []

        for i in range(1, 31):
            tarea, _ = Tarea.objects.get_or_create(
                titulo=f"Tarea {i}",
                defaults={
                    "descripcion": f"Descripción detallada de la tarea {i}",
                    "prioridad": (i % 5) + 1,
                    "estado": Tarea.Estado.PENDIENTE,
                    "completada": False,
                    "hora_vencimiento": time(17, 0),
                    "creador": usuarios[(i - 1) % 30],
                    "proyecto": proyectos[(i - 1) % 30],
                },
            )
            tareas.append(tarea)

            # Asociar una etiqueta a cada tarea
            tarea.etiquetas.add(etiquetas[(i - 1) % 30])

        # 5. Crear 30 asignaciones de tarea
        for i in range(30):
            AsignacionTarea.objects.get_or_create(
                tarea=tareas[i],
                usuario=usuarios[(i + 1) % 30],
                defaults={
                    "observaciones": (
                        f"Observaciones de la asignación {i + 1}"
                    ),
                },
            )

        # 6. Crear 30 colaboraciones de proyecto
        for i in range(30):
            ColaboracionProyecto.objects.get_or_create(
                usuario=usuarios[(i + 1) % 30],
                proyecto=proyectos[i],
            )

        # 7. Crear 30 comentarios
        for i in range(30):
            Comentario.objects.get_or_create(
                tarea=tareas[i],
                autor=usuarios[(i + 2) % 30],
                contenido=f"Comentario de ejemplo número {i + 1}",
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Seeder ejecutado correctamente."
            )
        )

        self.stdout.write(
            "Se han comprobado los registros de los siete modelos."
        )