# Generated by Django 5.2.3 on 2025-07-04 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data', models.DateField(unique=True)),
                ('recorrente', models.BooleanField(default=False, help_text='Se marcado, o feriado se repete anualmente')),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Feriado',
                'verbose_name_plural': 'Feriados',
                'ordering': ['data'],
            },
        ),
        migrations.CreateModel(
            name='HorarioFuncionamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.IntegerField(choices=[(0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'), (3, 'Quinta-feira'), (4, 'Sexta-feira'), (5, 'Sábado'), (6, 'Domingo')], unique=True)),
                ('hora_abertura', models.TimeField()),
                ('hora_fechamento', models.TimeField()),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Horário de Funcionamento',
                'verbose_name_plural': 'Horários de Funcionamento',
                'ordering': ['dia_semana'],
            },
        ),
    ]
