# Generated by Django 5.1 on 2024-09-20 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_blogcontentblock_header_level_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcontentblock',
            name='content_type',
        ),
    ]