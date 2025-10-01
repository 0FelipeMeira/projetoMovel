from django.db import models

class Registro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=128)
    
    def __str__(self):
        return self.nome

class RegistroMed(models.Model):
    medicamento = models.CharField(max_length=100)
    dosagem = models.FloatField()
    data_inicio = models.DateField()
    data_termino = models.DateField()
    horario = models.IntegerField()
    imagem = models.ImageField()

    def __str__(self):
        return self.medicamento
    
