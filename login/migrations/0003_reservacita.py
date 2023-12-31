# Generated by Django 4.2.4 on 2023-10-18 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0002_opinion_sentimiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservaCita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_entrega', models.TimeField()),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.service')),
                ('taller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas_como_taller', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas_como_usuario', to=settings.AUTH_USER_MODEL)),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.vehiculos')),
            ],
        ),
    ]
