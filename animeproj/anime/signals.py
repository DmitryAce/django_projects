from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver
from .models import Anime, AnimeCategory, AnimeTheme, AnimeEpisode
from django.db.models.signals import post_save, post_delete
from django.db import transaction

@receiver(m2m_changed, sender=Anime.genre.through)
def update_category_count(sender, instance, action, reverse, model, pk_set, **kwargs):
    # Если изменяется жанр у аниме (post_add, post_remove, post_clear)
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Обновляем категории, связанные с аниме
        if action == 'post_add':
            categories = AnimeCategory.objects.filter(pk__in=pk_set)
        elif action == 'post_remove':
            categories = AnimeCategory.objects.filter(pk__in=pk_set)
        else:
            categories = instance.genre.all()

        for category in categories:
            category.cnt = category.animes.count()
            category.save()

    # Если происходит полное удаление всех жанров у аниме
    if action == 'post_clear':
        for category in AnimeCategory.objects.all():
            category.cnt = category.animes.count()
            category.save()


@receiver(m2m_changed, sender=Anime.theme.through)
def update_theme_count(sender, instance, action, reverse, model, pk_set, **kwargs):
    # Если изменяется тема у аниме (post_add, post_remove, post_clear)
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Обновляем темы, связанные с аниме
        if action == 'post_add':
            themes = AnimeTheme.objects.filter(pk__in=pk_set)
        elif action == 'post_remove':
            themes = AnimeTheme.objects.filter(pk__in=pk_set)
        else:
            themes = instance.theme.all()

        for theme in themes:
            theme.cnt = theme.animes.count()
            theme.save()

    # Если происходит полное удаление всех жанров у аниме
    if action == 'post_clear':
        for category in AnimeCategory.objects.all():
            category.cnt = category.animes.count()
            category.save()


@receiver(post_save, sender=AnimeEpisode)
@receiver(post_delete, sender=AnimeEpisode)
def update_available_episodes(sender, instance, **kwargs):
    with transaction.atomic():
        anime = instance.anime
        anime.update_episodes()


@receiver(pre_delete, sender=Anime)
def update_count_on_delete(sender, instance, **kwargs):
    categories = list(instance.genre.all())
    themes = list(instance.theme.all())

    for category in categories:
        category.cnt = category.animes.count() - 1
        category.save()
    
    for theme in themes:
        theme.cnt = theme.animes.count() - 1
        theme.save()