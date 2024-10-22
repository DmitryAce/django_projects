# Generated by Django 5.1 on 2024-09-01 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0010_anime_comment_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimeEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('season', models.PositiveIntegerField(default=0)),
                ('episode', models.PositiveIntegerField(default=0)),
                ('video_file', models.FileField(blank=True, upload_to='episodes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='anime.anime')),
            ],
            options={
                'verbose_name_plural': 'Anime Episodes',
                'ordering': ('anime', 'season', 'episode'),
                'unique_together': {('anime', 'season', 'episode')},
            },
        ),
    ]
