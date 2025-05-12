from django.contrib import admin
from.models import Mantenimiento, Actividad, Usuario, Observacion

# Register your models here.
admin.site.register(Mantenimiento)
admin.site.register(Actividad)
admin.site.register(Usuario)
admin.site.register(Observacion)