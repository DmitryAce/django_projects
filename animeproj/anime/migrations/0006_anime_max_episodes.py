# Generated by Django 5.1 on 2024-08-29 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0005_alter_animecategory_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='max_episodes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
