from django.contrib import admin
from .models import Registro, Idoso, Medicamento, Horario, Tomada


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email")
    search_fields = ("nome", "email")


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 0


@admin.register(Idoso)
class IdosoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "responsavel", "criado_em")
    list_filter = ("responsavel",)
    search_fields = ("nome",)


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "idoso", "frequencia_tipo", "ativo")
    list_filter = ("frequencia_tipo", "ativo")
    search_fields = ("nome", "idoso__nome")
    inlines = [HorarioInline]


@admin.register(Tomada)
class TomadaAdmin(admin.ModelAdmin):
    list_display = ("id", "idoso", "medicamento", "horario_previsto", "tomado")
    list_filter = ("tomado", "medicamento")
    search_fields = ("idoso__nome", "medicamento__nome")
