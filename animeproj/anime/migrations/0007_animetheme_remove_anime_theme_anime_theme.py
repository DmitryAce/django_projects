# Generated by Django 5.1 on 2024-08-30 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0006_anime_max_episodes'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimeTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('cnt', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Anime Themes',
                'ordering': ('name',),
            },
        ),
        migrations.RemoveField(
            model_name='anime',
            name='theme',
        ),
        migrations.AddField(
            model_name='anime',
            name='theme',
            field=models.ManyToManyField(related_name='animes', to='anime.animetheme'),
        ),
    ]
