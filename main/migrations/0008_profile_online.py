# Generated by Django 3.2.8 on 2021-11-12 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20211107_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]
