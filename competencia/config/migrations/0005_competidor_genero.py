# Generated by Django 2.1.4 on 2019-02-23 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_genero'),
    ]

    operations = [
        migrations.AddField(
            model_name='competidor',
            name='genero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='config.Genero'),
        ),
    ]
