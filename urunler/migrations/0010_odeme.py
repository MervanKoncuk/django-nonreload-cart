# Generated by Django 4.1.3 on 2022-11-14 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('urunler', '0009_sepet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Odeme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toplamFiyat', models.IntegerField()),
                ('sepet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urunler.sepet')),
            ],
        ),
    ]