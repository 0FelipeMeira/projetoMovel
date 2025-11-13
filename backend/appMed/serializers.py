from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
    Registro,
    Idoso,
    Medicamento,
    Horario,
    Tomada,
)

class RegistroSerializer(serializers.ModelSerializer):
    confirmar_senha = serializers.CharField(write_only=True)  # apenas para validação

    class Meta:
        model = Registro
        fields = ['id', 'nome', 'email', 'senha', 'confirmar_senha']
        extra_kwargs = {
            'senha': {'write_only': True}  # para não retornar a senha no GET
        }

    def validate_email(self, value):
        # validação explícita para retornar erro amigável antes da constraint do banco
        qs = Registro.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('E-mail já cadastrado.')
        return value

    def validate(self, data):
        if data['senha'] != data['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirmar_senha')  # não salva no DB
        senha = validated_data.pop('senha')
        registro = Registro(**validated_data)
        registro.senha = make_password(senha)
        registro.save()
        return registro

    def update(self, instance, validated_data):
        senha = validated_data.pop('senha', None)
        validated_data.pop('confirmar_senha', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if senha:
            instance.senha = make_password(senha)

        instance.save()
        return instance

class IdosoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idoso
        fields = ['id', 'responsavel', 'nome', 'data_nascimento', 'observacoes', 'criado_em']


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ['id', 'hora']


class MedicamentoSerializer(serializers.ModelSerializer):
    horarios = HorarioSerializer(many=True, required=False)

    class Meta:
        model = Medicamento
        fields = [
            'id', 'idoso', 'nome', 'dosagem', 'data_inicio', 'data_termino',
            'frequencia_tipo', 'intervalo_horas', 'dias_semana', 'ativo', 'criado_em',
            'horarios',
        ]

    def validate(self, attrs):
        freq = attrs.get('frequencia_tipo', getattr(self.instance, 'frequencia_tipo', None))
        intervalo = attrs.get('intervalo_horas', getattr(self.instance, 'intervalo_horas', None))
        if freq == 'intervalo_horas' and not intervalo:
            raise serializers.ValidationError({'intervalo_horas': 'Obrigatório quando frequencia_tipo=intervalo_horas.'})
        return attrs

    def create(self, validated_data):
        horarios_data = validated_data.pop('horarios', [])
        medicamento = Medicamento.objects.create(**validated_data)
        for h in horarios_data:
            Horario.objects.create(medicamento=medicamento, **h)
        return medicamento

    def update(self, instance, validated_data):
        horarios_data = validated_data.pop('horarios', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if horarios_data is not None:
            instance.horarios.all().delete()
            for h in horarios_data:
                Horario.objects.create(medicamento=instance, **h)
        return instance


class TomadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tomada
        fields = [
            'id', 'medicamento', 'idoso', 'horario_previsto', 'tomado',
            'data_hora_tomada', 'observacao', 'criado_por', 'criado_em'
        ]
