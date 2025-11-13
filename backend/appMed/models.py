from django.db import models


class Registro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    senha = models.CharField(max_length=128)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Idoso(models.Model):
    responsavel = models.ForeignKey(Registro, related_name='idosos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=120)
    data_nascimento = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True, default='')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} (resp: {self.responsavel.nome})"


class Medicamento(models.Model):
    FREQ_TIPO_CHOICES = (
        ('horarios_fixos', 'Horários fixos'),
        ('intervalo_horas', 'Intervalo em horas'),
    )

    idoso = models.ForeignKey(Idoso, related_name='medicamentos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=120)
    dosagem = models.CharField(max_length=80)
    data_inicio = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    frequencia_tipo = models.CharField(max_length=20, choices=FREQ_TIPO_CHOICES, default='horarios_fixos')
    intervalo_horas = models.PositiveIntegerField(null=True, blank=True)
    dias_semana = models.CharField(max_length=50, blank=True, default='')  # ex: "SEG,TER,QUA"
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.idoso.nome}"


class Horario(models.Model):
    medicamento = models.ForeignKey(Medicamento, related_name='horarios', on_delete=models.CASCADE)
    hora = models.TimeField()

    def __str__(self):
        return f"{self.medicamento.nome} @ {self.hora}"


class Tomada(models.Model):
    medicamento = models.ForeignKey(Medicamento, related_name='tomadas', on_delete=models.CASCADE)
    idoso = models.ForeignKey(Idoso, related_name='tomadas', on_delete=models.CASCADE)
    horario_previsto = models.DateTimeField()
    tomado = models.BooleanField(default=False)
    data_hora_tomada = models.DateTimeField(null=True, blank=True)
    observacao = models.TextField(blank=True, default='')
    criado_por = models.ForeignKey(Registro, null=True, blank=True, on_delete=models.SET_NULL, related_name='tomadas_registradas')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = 'Tomado' if self.tomado else 'Pendente'
        return f"{self.idoso.nome} - {self.medicamento.nome} ({status})"
