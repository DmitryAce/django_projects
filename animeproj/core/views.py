from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count, Case, When, IntegerField, Max
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework.views import APIView

from fuzzywuzzy import fuzz
from datetime import timedelta

from anime.models import *
from anime.serializers import *


PAGINATION = 6
SECOND_PAGINATION = 8
COMMENTED_ANIME = 10
PERIODIC_ANIME = 3

def paginate_queryset(request, queryset, per_page=10):
    """Пагинация"""
    paginator = Paginator(queryset, per_page)
    page = request.GET.get("page", 1)

    try:
        paginated_data = paginator.page(page)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    return paginated_data, paginator


def get_top_anime_by_views():
    """Топ аниме по просмотрам"""
    top_anime_views = AnimeViewCount.objects.order_by("-views")
    top_anime_ids = [view_count.anime.id for view_count in top_anime_views]
    return Anime.objects.filter(id__in=top_anime_ids).order_by(
        Case(
            *[
                When(id=anime_id, then=pos)
                for pos, anime_id in enumerate(top_anime_ids)
            ],
            output_field=IntegerField()
        )
    )


def get_weighted_anime_with_ratings(limit=PAGINATION):
    """Получение списка аниме с рейтингом"""
    global_avg_rating = Anime.objects.aggregate(Avg("rating"))["rating__avg"]
    min_ratings_for_weight = 10
    recent_ratings = AnimeRating.objects.all()

    anime_with_ratings = (
        recent_ratings.values("anime")
        .annotate(avg_rating=Avg("rating"), rating_count=Count("rating"))
        .order_by("-avg_rating")
    )

    weighted_anime_with_ratings = []
    for entry in anime_with_ratings:
        avg_rating = entry["avg_rating"]
        rating_count = entry["rating_count"]
        weighted_rating = (
            (avg_rating * rating_count) + (global_avg_rating * min_ratings_for_weight)
        ) / (rating_count + min_ratings_for_weight)
        weighted_anime_with_ratings.append(
            {"anime": entry["anime"], "weighted_rating": weighted_rating}
        )

    top_anime_ids = [
        entry["anime"]
        for entry in sorted(
            weighted_anime_with_ratings,
            key=lambda x: x["weighted_rating"],
            reverse=True,
        )[:limit]
    ]
    return Anime.objects.filter(id__in=top_anime_ids)


class IndexView(APIView):
    """
    get:
    Возвращает все необходимые списки аниме для главной страницы
    """

    def get(self, request, *args, **kwargs):
        two_weeks_ago = timezone.now() - timedelta(weeks=2)
        recent_ratings = AnimeRating.objects.filter(created_at__gte=two_weeks_ago)
        anime_with_ratings = (
            recent_ratings.values("anime")
            .annotate(avg_rating=Avg("rating"), rating_count=Count("rating"))
            .order_by("-avg_rating")[:PAGINATION]
        )
        anime_ids = [entry["anime"] for entry in anime_with_ratings]
        preserved_order = Case(
            *[When(id=anime_id, then=pos) for pos, anime_id in enumerate(anime_ids)]
        )
        most_favorited_recently = Anime.objects.filter(id__in=anime_ids).order_by(
            preserved_order
        )
        avg_rating_map = {
            entry["anime"]: entry["avg_rating"] for entry in anime_with_ratings
        }
        for anime in most_favorited_recently:
            anime.avg_rating = avg_rating_map.get(anime.id, 0)
        recently_added = Anime.objects.order_by("-add_time")[:PAGINATION]
        most_favorited = get_weighted_anime_with_ratings()
        top_anime = get_top_anime_by_views()[:PAGINATION]
        top_daily_animes = Anime.objects.select_related("view_count").order_by(
            "-view_count__daily_views"
        )[:PERIODIC_ANIME]
        top_weekly_animes = Anime.objects.select_related("view_count").order_by(
            "-view_count__weekly_views"
        )[:PERIODIC_ANIME]
        top_monthly_animes = Anime.objects.select_related("view_count").order_by(
            "-view_count__monthly_views"
        )[:PERIODIC_ANIME]
        top_yearly_animes = Anime.objects.select_related("view_count").order_by(
            "-view_count__yearly_views"
        )[:PERIODIC_ANIME]
        commented_anime = Anime.objects.annotate(
            latest_comment_date=Max("comments__created_at")
        ).order_by("-latest_comment_date")[:COMMENTED_ANIME]

        return render(
            request,
            "core/index.html",
            {
                "most_favorited_recently": most_favorited_recently,
                "recently_added": recently_added,
                "most_favorited": most_favorited,
                "top_viewed": top_anime,
                "top_daily_animes": top_daily_animes,
                "top_weekly_animes": top_weekly_animes,
                "top_monthly_animes": top_monthly_animes,
                "top_yearly_animes": top_yearly_animes,
                "commented_anime": commented_anime,
            },
        )


class SearchView(APIView):
    """
    get:
    Перенаправляет на страницу с результатом поиска
    """

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        return redirect("core:general", order_by=query)


class CategoryView(APIView):
    """
    get:
    Возвращает все необходимые списки аниме для страницы категории
    """

    def get(self, request, pk, *args, **kwargs):
        category = get_object_or_404(AnimeCategory, pk=pk)
        animes_in_category = Anime.objects.filter(genre__pk=pk)
        order_by = request.GET.get("order_by", "title")

        if order_by == "view_count":
            animes_in_category = animes_in_category.order_by("-view_count__views")
        elif order_by == "release_date":
            animes_in_category = animes_in_category.order_by("-release_date")
        else:
            animes_in_category = animes_in_category.order_by("title")

        top_daily_animes = (
            Anime.objects.filter(genre__pk=pk)
            .select_related("view_count")
            .order_by("-view_count__daily_views")[:PERIODIC_ANIME]
        )
        top_weekly_animes = (
            Anime.objects.filter(genre__pk=pk)
            .select_related("view_count")
            .order_by("-view_count__weekly_views")[:PERIODIC_ANIME]
        )
        top_monthly_animes = (
            Anime.objects.filter(genre__pk=pk)
            .select_related("view_count")
            .order_by("-view_count__monthly_views")[:PERIODIC_ANIME]
        )
        top_yearly_animes = (
            Anime.objects.filter(genre__pk=pk)
            .select_related("view_count")
            .order_by("-view_count__yearly_views")[:PERIODIC_ANIME]
        )
        commented_anime = (
            Anime.objects.filter(genre__pk=pk)
            .annotate(latest_comment_date=Max("comments__created_at"))
            .order_by("-latest_comment_date")[:COMMENTED_ANIME]
        )

        animes, paginator = paginate_queryset(request, animes_in_category, SECOND_PAGINATION)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "core/anime_list.html", {"animes": animes, "paginator": paginator}
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "core/category.html",
            {
                "category": category,
                "animes": animes,
                "top_daily_animes": top_daily_animes,
                "top_weekly_animes": top_weekly_animes,
                "top_monthly_animes": top_monthly_animes,
                "top_yearly_animes": top_yearly_animes,
                "commented_anime": commented_anime,
                "selected_order_by": order_by,
                "paginator": paginator,
            },
        )


class GeneralView(APIView):
    """
    get:
    Возвращает список аниме в зависимости от запроса
    """

    def get(self, request, order_by, *args, **kwargs):
        all_anime = Anime.objects.all()
        title = "Результаты поиска"

        if order_by == "most_favorited_recently":
            title = "Сейчас в тренде"
            two_weeks_ago = timezone.now() - timedelta(weeks=2)
            recent_ratings = AnimeRating.objects.filter(created_at__gte=two_weeks_ago)
            anime_with_ratings = (
                recent_ratings.values("anime")
                .annotate(avg_rating=Avg("rating"), rating_count=Count("rating"))
                .order_by("-avg_rating")
            )
            anime_ids = [entry["anime"] for entry in anime_with_ratings]
            preserved_order = Case(
                *[When(id=anime_id, then=pos) for pos, anime_id in enumerate(anime_ids)]
            )
            animes = Anime.objects.filter(id__in=anime_ids).order_by(preserved_order)
            avg_rating_map = {
                entry["anime"]: entry["avg_rating"] for entry in anime_with_ratings
            }
            for anime in animes:
                anime.avg_rating = avg_rating_map.get(anime.id, 0)
        elif order_by == "top_viewed":
            title = "Популярные"
            animes = get_top_anime_by_views()
        elif order_by == "recently_added":
            title = "Недавно добавленные"
            animes = Anime.objects.order_by("-add_time")
        elif order_by == "most_favorited":
            title = "Наиболее оцененные"
            animes = get_weighted_anime_with_ratings()
        else:
            animes = [
                (
                    anime,
                    (
                        fuzz.ratio(order_by, anime.title)
                        + fuzz.partial_ratio(order_by, anime.title)
                        + fuzz.token_sort_ratio(order_by, anime.title)
                    )
                    / 3,
                )
                for anime in all_anime
            ]
            animes.sort(key=lambda x: x[1], reverse=True)
            animes = [anime for anime, _ in animes]

        animes, paginator = paginate_queryset(request, animes, SECOND_PAGINATION)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "core/general_list.html", {"animes": animes, "paginator": paginator}
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "core/general.html",
            {"title": title, "animes": animes, "paginator": paginator},
        )


class CategoriesView(APIView):
    """
    get:
    Возвращает список категорий
    """

    def get(self, request, *args, **kwargs):
        categories = AnimeCategory.objects.all()
        return render(request, "core/categories.html", {"categories": categories})
