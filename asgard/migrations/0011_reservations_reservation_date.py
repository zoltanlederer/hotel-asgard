# Generated by Django 3.1.7 on 2021-07-24 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asgard', '0010_auto_20210724_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservations',
            name='reservation_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]