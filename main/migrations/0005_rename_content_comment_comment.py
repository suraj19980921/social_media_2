# Generated by Django 3.2.8 on 2021-11-06 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_content_post_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='comment',
        ),
    ]
