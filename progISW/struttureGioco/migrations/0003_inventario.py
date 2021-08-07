# Generated by Django 2.2 on 2021-08-07 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('struttureGioco', '0002_personaggio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipaggiamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='struttureGioco.Equipaggiamento')),
                ('personaggio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='struttureGioco.Personaggio')),
            ],
        ),
    ]
