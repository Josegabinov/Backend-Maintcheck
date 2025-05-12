from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Mantenimiento, Actividad, Usuario, Observacion
from datetime import datetime

class ObservacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacion
        fields = ['id', 'texto', 'fecha_creacion']

class ActividadSerializer(serializers.ModelSerializer):
    observaciones = ObservacionSerializer(many=True, read_only=True)  # Incluir observaciones en actividades

    class Meta:
        model = Actividad
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'observaciones']

    def validate(self, data):
        # Validar que las fechas sean válidas
        if 'fecha_inicio' in data and 'fecha_fin' in data:
            if data['fecha_inicio'] > data['fecha_fin']:
                raise serializers.ValidationError({
                    "fecha": "La fecha de inicio no puede ser posterior a la fecha de fin"
                })

        # Si la actividad está asociada a un mantenimiento, validar sus fechas
        mantenimiento = self.context.get('mantenimiento')
        if mantenimiento and 'fecha_inicio' in data and 'fecha_fin' in data:
            if data['fecha_inicio'] < mantenimiento.fecha_inicio:
                raise serializers.ValidationError({
                    "fecha_inicio": f"La fecha de inicio debe ser posterior a la fecha de inicio del mantenimiento ({mantenimiento.fecha_inicio})"
                })
            if data['fecha_fin'] > mantenimiento.fecha_fin:
                raise serializers.ValidationError({
                    "fecha_fin": f"La fecha de fin debe ser anterior a la fecha de fin del mantenimiento ({mantenimiento.fecha_fin})"
                })

        return data

class MantenimientoSerializer(serializers.ModelSerializer):
    actividades = ActividadSerializer(many=True, read_only=True)
    observaciones = ObservacionSerializer(many=True, read_only=True)  # Incluir observaciones en mantenimientos

    class Meta:
        model = Mantenimiento
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 
                  'estado', 'responsable', 'actividades', 'observaciones']

    def validate(self, data):
        # Validar formato de fechas y que inicio sea anterior a fin
        if 'fecha_inicio' in data and 'fecha_fin' in data:
            if data['fecha_inicio'] > data['fecha_fin']:
                raise serializers.ValidationError({
                    "fecha": "La fecha de inicio no puede ser posterior a la fecha de fin"
                })

        # Validar las fechas de las actividades al crear/actualizar mantenimiento
        actividades_data = self.initial_data.get('actividades', [])
        for actividad in actividades_data:
            if isinstance(actividad, dict) and 'id' not in actividad:
                fecha_inicio_act = actividad.get('fecha_inicio')
                fecha_fin_act = actividad.get('fecha_fin')
                
                if fecha_inicio_act and fecha_fin_act:
                    try:
                        fecha_inicio_act = datetime.fromisoformat(fecha_inicio_act.replace('Z', '+00:00'))
                        fecha_fin_act = datetime.fromisoformat(fecha_fin_act.replace('Z', '+00:00'))
                        
                        if fecha_inicio_act < data['fecha_inicio']:
                            raise serializers.ValidationError({
                                "actividades": f"La actividad '{actividad.get('nombre')}' no puede comenzar antes que el mantenimiento"
                            })
                        if fecha_fin_act > data['fecha_fin']:
                            raise serializers.ValidationError({
                                "actividades": f"La actividad '{actividad.get('nombre')}' no puede terminar después que el mantenimiento"
                            })
                    except ValueError:
                        raise serializers.ValidationError({
                            "actividades": f"Formato de fecha inválido para la actividad '{actividad.get('nombre')}'"
                        })

        return data

    def create(self, validated_data):
        actividades_data = self.initial_data.get('actividades', [])
        mantenimiento = Mantenimiento.objects.create(**validated_data)
        
        for actividad_item in actividades_data:
            if isinstance(actividad_item, dict):
                if 'id' in actividad_item:
                    try:
                        actividad = Actividad.objects.get(id=actividad_item['id'])
                        # Validar fechas de actividad existente
                        serializer = ActividadSerializer(
                            actividad, 
                            context={'mantenimiento': mantenimiento}
                        )
                        if serializer.is_valid(raise_exception=True):
                            mantenimiento.actividades.add(actividad)
                    except Actividad.DoesNotExist:
                        continue
                else:
                    # Crear nueva actividad con validación
                    serializer = ActividadSerializer(
                        data=actividad_item,
                        context={'mantenimiento': mantenimiento}
                    )
                    if serializer.is_valid(raise_exception=True):
                        actividad = serializer.save()
                        mantenimiento.actividades.add(actividad)
        
        return mantenimiento

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']