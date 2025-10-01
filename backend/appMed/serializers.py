from rest_framework import serializers
from .models import Registro, RegistroMed
from django.contrib.auth.hashers import make_password

class RegistroSerializer(serializers.ModelSerializer):
    confirmar_senha = serializers.CharField(write_only=True)  # apenas para validação

    class Meta:
        model = Registro
        fields = ['id', 'nome', 'email', 'senha', 'confirmar_senha']
        extra_kwargs = {
            'senha': {'write_only': True}  # para não retornar a senha no GET
        }

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

class RegistroMedSerializer(serializers.ModelSerializer):
    class Meta: 
        model = RegistroMed
        fields = '__all__'
