# Generated by Django 4.2.4 on 2023-10-18 02:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('carro', 'Carro'), ('bicicleta', 'Bicicleta'), ('moto', 'Moto')], max_length=10)),
                ('modelo', models.CharField(blank=True, max_length=10, null=True)),
                ('año', models.IntegerField(blank=True, default=0, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(choices=[('Mantenimiento', 'Mantenimiento'), ('Cambio de aceite', 'Cambio de aceite'), ('Frenos', 'Frenos'), ('Suspensión', 'Suspensión')], max_length=50)),
                ('service_time', models.CharField(choices=[('1', '1 hora'), ('2', '2 horas'), ('3', '3 horas'), ('4', '4 horas'), ('5', '5 horas')], max_length=1)),
                ('service_price', models.CharField(choices=[('300-1000', '$300 - $1000'), ('1000-2000', '$1000 - $2000'), ('2000-3000', '$2000 - $3000')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExtendedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('direccion', models.CharField(blank=True, max_length=128, null=True)),
                ('cp', models.CharField(blank=True, max_length=5, null=True)),
                ('calidad', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('id_taller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opinions', to=settings.AUTH_USER_MODEL)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('id_taller', 'id_usuario')},
            },
        ),
    ]
