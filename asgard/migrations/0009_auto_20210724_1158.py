# Generated by Django 3.1.7 on 2021-07-24 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asgard', '0008_auto_20210724_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='reserved_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asgard.rooms'),
        ),
    ]