# Generated by Django 3.2.12 on 2022-10-12 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urunler', '0002_urun_resim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urun',
            name='resim',
            field=models.FileField(blank=True, null=True, upload_to='urunler/'),
        ),
    ]
