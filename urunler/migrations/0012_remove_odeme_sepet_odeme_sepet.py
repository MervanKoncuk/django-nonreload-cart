# Generated by Django 4.1.3 on 2022-11-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urunler', '0011_odeme_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='odeme',
            name='sepet',
        ),
        migrations.AddField(
            model_name='odeme',
            name='sepet',
            field=models.ManyToManyField(to='urunler.sepet'),
        ),
    ]
