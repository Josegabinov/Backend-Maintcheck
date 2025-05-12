from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Observacion(models.Model):
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    mantenimiento = models.ForeignKey('Mantenimiento', on_delete=models.CASCADE, null=True, blank=True, related_name='observaciones')
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, null=True, blank=True, related_name='observaciones')

class Actividad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(null=True, blank=True)  # Fecha y hora de inicio
    fecha_fin = models.DateTimeField(null=True, blank=True)  # Fecha y hora de fin

    def __str__(self):
        return self.nombre

class Mantenimiento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(null=True, blank=True)  # Fecha y hora de inicio
    fecha_fin = models.DateTimeField(null=True, blank=True)  # Fecha y hora de fin
    estado = models.CharField(max_length=50, default="pendiente")  # Estado del mantenimiento
    responsable = models.CharField(max_length=255)
    actividades = models.ManyToManyField(Actividad)  # Relación con actividades
    es_version_original = models.BooleanField(default=False)  # Indica si es la versión original

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario debe ser proporcionado')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, default='default_username')  # Añadir un valor por defecto
    password = models.CharField(max_length=128, default='default_password')
    rol = models.CharField(max_length=20, choices=[('gerente', 'Gerente'), ('operador', 'Operador'), ('supervisor', 'Supervisor')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username