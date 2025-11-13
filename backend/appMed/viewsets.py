from datetime import datetime, time
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Registro,
    Idoso,
    Medicamento,
    Horario,
    Tomada,
)
from .serializers import (
    RegistroSerializer,
    IdosoSerializer,
    MedicamentoSerializer,
    TomadaSerializer,
)


class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        if registro:
            return Registro.objects.filter(id=registro.id)
        return Registro.objects.none()


class IdosoViewSet(viewsets.ModelViewSet):
    queryset = Idoso.objects.all().select_related('responsavel')
    serializer_class = IdosoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        if registro:
            qs = qs.filter(responsavel=registro)
        else:
            qs = qs.none()
        return qs

    def perform_update(self, serializer):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        instance = self.get_object()
        if not registro or instance.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para este idoso.')
        serializer.save()

    def perform_destroy(self, instance):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        if not registro or instance.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para este idoso.')
        instance.delete()
    def perform_create(self, serializer):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        if not registro:
            raise PermissionDenied('Não autenticado.')
        serializer.save(responsavel=registro)

    @action(detail=True, methods=['get'], url_path='agenda')
    def agenda(self, request, pk=None):
        idoso = self.get_object()
        data_str = request.query_params.get('data')
        try:
            data_base = datetime.strptime(data_str, '%Y-%m-%d').date() if data_str else timezone.localdate()
        except ValueError:
            return Response({'detail': 'Parâmetro data inválido (YYYY-MM-DD).'}, status=status.HTTP_400_BAD_REQUEST)

        itens = []
        medicamentos = idoso.medicamentos.filter(ativo=True)
        for med in medicamentos:
            # Considera apenas horários fixos para agenda do dia
            if med.frequencia_tipo == 'horarios_fixos':
                for h in med.horarios.all():
                    dt_prev = datetime.combine(data_base, h.hora, tzinfo=timezone.get_current_timezone())
                    # Verifica janela de datas
                    if med.data_inicio and data_base < med.data_inicio:
                        continue
                    if med.data_termino and data_base > med.data_termino:
                        continue
                    # Se dias_semana definido, filtra
                    if med.dias_semana:
                        # Ex.: SEG,TER,QUA (segunda=0)
                        mapa = ['SEG','TER','QUA','QUI','SEX','SAB','DOM']
                        hoje_tag = mapa[data_base.weekday()]
                        permitidos = [s.strip().upper() for s in med.dias_semana.split(',') if s.strip()]
                        if permitidos and hoje_tag not in permitidos:
                            continue
                    # Busca tomada já registrada para esse horário previsto
                    tomada = Tomada.objects.filter(idoso=idoso, medicamento=med, horario_previsto=dt_prev).first()
                    itens.append({
                        'medicamento_id': med.id,
                        'medicamento': med.nome,
                        'dosagem': med.dosagem,
                        'horario_previsto': dt_prev,
                        'tomado': bool(tomada and tomada.tomado),
                        'tomada_id': tomada.id if tomada else None,
                    })
        return Response(itens)


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all().select_related('idoso').prefetch_related('horarios')
    serializer_class = MedicamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        if registro:
            qs = qs.filter(idoso__responsavel=registro)
        else:
            qs = qs.none()
        # opcionalmente ainda filtra por idoso=id quando query param for passado
        idoso_id = self.request.query_params.get('idoso')
        if idoso_id:
            qs = qs.filter(idoso_id=idoso_id)
        return qs

    def perform_create(self, serializer):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        idoso = serializer.validated_data.get('idoso')
        if not registro or not idoso or idoso.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para este idoso.')
        serializer.save()

    def perform_update(self, serializer):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        instance = self.get_object()
        if not registro or instance.idoso.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para este medicamento.')
        # se idoso for alterado, também validar
        idoso = serializer.validated_data.get('idoso', instance.idoso)
        if idoso.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para este idoso (alteração).')
        serializer.save()

    def perform_destroy(self, instance):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        if not registro or instance.idoso.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para este medicamento.')
        instance.delete()

    @action(detail=True, methods=['post'], url_path='registrar-tomada')
    def registrar_tomada(self, request, pk=None):
        medicamento = self.get_object()
        idoso = medicamento.idoso
        # impede alterar medicamentos de outro responsável
        user = getattr(request, 'user', None)
        registro = getattr(user, 'registro', None)
        if not registro or idoso.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para este idoso.')
        horario_previsto = request.data.get('horario_previsto')
        tomado = request.data.get('tomado', True)
        observacao = request.data.get('observacao', '')

        if not horario_previsto:
            return Response({'detail': 'horario_previsto é obrigatório (ISO 8601).'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            dt_prev = datetime.fromisoformat(horario_previsto)
            if dt_prev.tzinfo is None:
                dt_prev = timezone.make_aware(dt_prev, timezone.get_current_timezone())
        except Exception:
            return Response({'detail': 'Formato de horario_previsto inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        tomada_obj, created = Tomada.objects.get_or_create(
            medicamento=medicamento,
            idoso=idoso,
            horario_previsto=dt_prev,
            defaults={
                'tomado': bool(tomado),
                'data_hora_tomada': timezone.now() if tomado else None,
                'observacao': observacao,
            }
        )
        if not created:
            tomada_obj.tomado = bool(tomado)
            tomada_obj.data_hora_tomada = timezone.now() if tomado else None
            tomada_obj.observacao = observacao
            tomada_obj.save()

        return Response(TomadaSerializer(tomada_obj).data, status=status.HTTP_200_OK)


class TomadaViewSet(viewsets.ModelViewSet):
    queryset = Tomada.objects.all().select_related('idoso', 'medicamento')
    serializer_class = TomadaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        idoso_id = self.request.query_params.get('idoso')
        medicamento_id = self.request.query_params.get('medicamento')
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        if registro:
            qs = qs.filter(idoso__responsavel=registro)
        else:
            qs = qs.none()
        if idoso_id:
            qs = qs.filter(idoso_id=idoso_id)
        if medicamento_id:
            qs = qs.filter(medicamento_id=medicamento_id)
        return qs

    def perform_create(self, serializer):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        idoso = serializer.validated_data.get('idoso')
        if not registro or not idoso or idoso.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para este idoso.')
        serializer.save(criado_por=registro)

    def perform_update(self, serializer):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        instance = self.get_object()
        if not registro or instance.idoso.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para esta tomada.')
        serializer.save()

    def perform_destroy(self, instance):
        user = getattr(self.request, 'user', None)
        registro = getattr(user, 'registro', None)
        if not registro or instance.idoso.responsavel_id != registro.id:
            raise PermissionDenied('Sem permissão para esta tomada.')
        instance.delete()

