# Generated by Django 5.1 on 2024-09-20 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcontentblock',
            name='header_level',
        ),
        migrations.AddField(
            model_name='blogcontentblock',
            name='header',
            field=models.TextField(blank=True, null=True),
        ),
    ]
