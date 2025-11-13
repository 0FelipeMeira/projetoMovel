from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appMed', '0003_horario_idoso_medicamento_tomada_delete_registromed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registro',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registro',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]

