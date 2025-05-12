from rest_framework import viewsets
from rest_framework.decorators import api_view
from .models import Mantenimiento, Actividad, Usuario, Observacion
from .serializer import MantenimientoSerializer, ActividadSerializer,ObservacionSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404



class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

class CargarMantenimientosView(APIView):
    def post(self, request):
        try:
            if not isinstance(request.data, list):
                return Response(
                    {"error": "El archivo debe contener una lista de mantenimientos."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            mantenimientos_creados = []
            errores = []

            for index, mantenimiento_data in enumerate(request.data):
                try:
                    serializer = MantenimientoSerializer(data=mantenimiento_data)
                    
                    if serializer.is_valid():
                        try:
                            mantenimiento = serializer.save()
                            mantenimientos_creados.append(serializer.data)
                        except Exception as save_error:
                            errores.append({
                                "indice": index,
                                "error": f"Error al guardar: {str(save_error)}",
                                "data": mantenimiento_data
                            })
                    else:
                        errores.append({
                            "indice": index,
                            "error": serializer.errors,
                            "data": mantenimiento_data
                        })
                except Exception as item_error:
                    errores.append({
                        "indice": index,
                        "error": str(item_error),
                        "data": mantenimiento_data
                    })

            if errores:
                return Response({
                    "message": "Algunos mantenimientos no se pudieron cargar.",
                    "mantenimientos_creados": mantenimientos_creados,
                    "errores": errores
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "Todos los mantenimientos se cargaron correctamente.",
                "mantenimientos_creados": mantenimientos_creados
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({
                "error": "Error inesperado al cargar mantenimientos.",
                "detalle": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

class RegistrarInicioFinMantenimientoView(APIView):
    def post(self, request, mantenimiento_id):
        try:
            mantenimiento = Mantenimiento.objects.get(id=mantenimiento_id)
            fecha_inicio = request.data.get('fecha_inicio')
            fecha_fin = request.data.get('fecha_fin')

            if fecha_inicio:
                mantenimiento.fecha_inicio = fecha_inicio
            if fecha_fin:
                mantenimiento.fecha_fin = fecha_fin

            mantenimiento.save()
            return Response({"message": "Fecha registrada correctamente."}, status=status.HTTP_200_OK)
        except Mantenimiento.DoesNotExist:
            return Response({"error": "Mantenimiento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

class RegistrarInicioFinActividadView(APIView):
    def post(self, request, actividad_id):
        try:
            actividad = Actividad.objects.get(id=actividad_id)
            data = request.data

            # Solo actualizamos fechas de inicio o fin
            if 'fecha_inicio' in data:
                actividad.fecha_inicio = data['fecha_inicio']
            if 'fecha_fin' in data:
                actividad.fecha_fin = data['fecha_fin']
            
            actividad.save()
            return Response({"message": "Fecha actualizada correctamente."}, status=status.HTTP_200_OK)
        except Actividad.DoesNotExist:
            return Response({"error": "Actividad no encontrada."}, status=status.HTTP_404_NOT_FOUND)

class ActividadInicioFinView(APIView):
    def post(self, request, actividad_id):
        try:
            actividad = Actividad.objects.get(id=actividad_id)
            if 'fecha_inicio' in request.data:
                actividad.fecha_inicio = request.data['fecha_inicio']
            if 'fecha_fin' in request.data:
                actividad.fecha_fin = request.data['fecha_fin']
            actividad.save()
            return Response({"message": "Fecha actualizada correctamente."}, status=status.HTTP_200_OK)
        except Actividad.DoesNotExist:
            return Response({"error": "Actividad no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        

class CrearActividadesView(APIView):
    def post(self, request):
        try:
            if not isinstance(request.data, list):
                return Response(
                    {"error": "El cuerpo de la solicitud debe ser una lista de actividades."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actividades_data = request.data
            actividades_creadas = []
            errores = []

            for actividad_data in actividades_data:
                serializer = ActividadSerializer(data=actividad_data)
                if serializer.is_valid():
                    actividad = serializer.save()
                    actividades_creadas.append(serializer.data)
                else:
                    errores.append({
                        "data": actividad_data,
                        "errors": serializer.errors
                    })

            if errores:
                return Response({
                    "message": "Algunas actividades no se pudieron crear.",
                    "actividades_creadas": actividades_creadas,
                    "errores": errores
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "Todas las actividades se crearon correctamente.",
                "actividades_creadas": actividades_creadas
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": "Error inesperado al crear actividades.", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ObservacionMantenimientoView(APIView):
    def post(self, request, mantenimiento_id):
        try:
            mantenimiento = Mantenimiento.objects.get(id=mantenimiento_id)
            texto = request.data.get('texto')
            if texto:
                observacion = Observacion.objects.create(mantenimiento=mantenimiento, texto=texto)
                serializer = ObservacionSerializer(observacion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Texto de la observación no proporcionado."}, status=status.HTTP_400_BAD_REQUEST)
        except Mantenimiento.DoesNotExist:
            return Response({"error": "Mantenimiento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

class ObservacionActividadView(APIView):
    def post(self, request, actividad_id):
        try:
            actividad = Actividad.objects.get(id=actividad_id)
            texto = request.data.get('texto')
            if texto:
                observacion = Observacion.objects.create(actividad=actividad, texto=texto)
                serializer = ObservacionSerializer(observacion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Texto de la observación no proporcionado."}, status=status.HTTP_400_BAD_REQUEST)
        except Actividad.DoesNotExist:
            return Response({"error": "Actividad no encontrada."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, actividad_id, observacion_id):
        try:
            observacion = Observacion.objects.get(id=observacion_id, actividad_id=actividad_id)
            texto = request.data.get('texto')
            if not texto:
                return Response({"error": "El texto no puede estar vacío."}, status=status.HTTP_400_BAD_REQUEST)
            observacion.texto = texto
            observacion.save()
            serializer = ObservacionSerializer(observacion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Observacion.DoesNotExist:
            return Response({"error": "Observación no encontrada."}, status=status.HTTP_404_NOT_FOUND)
class ObservacionDetailView(APIView):
    def put(self, request, observacion_id):
        try:
            observacion = Observacion.objects.get(id=observacion_id)
            texto = request.data.get('texto')
            if not texto:
                return Response({"error": "El texto no puede estar vacío."}, status=status.HTTP_400_BAD_REQUEST)
            observacion.texto = texto
            observacion.save()
            serializer = ObservacionSerializer(observacion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Observacion.DoesNotExist:
            return Response({"error": "Observación no encontrada."}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, 
        status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    serializer= UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data}, 
    status=status.HTTP_200_OK)

    
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   