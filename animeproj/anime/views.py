from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz

from .models import (
    Anime,
    AnimeComment,
    AnimeEpisode,
    AnimeRating,
    AnimeViewCount,
    AnimeFavorites,
)
from .forms import AnimeCommentForm

from user.models import UserProfile

COMMENT_PAGINATION = 6


class IndexView(APIView):
    """
    get:
    Возвращает данные для страницы деталей аниме

    post:
    Создает комментарий пользователя

    delete:
    Удаляет комментарий пользователя
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_might_like_anime(self, current_anime):
        all_anime = Anime.objects.exclude(id=current_anime.id)
        might_like = []

        def average_category_similarity(anime1, anime2):
            categories1 = set(anime1.genre.values_list("name", flat=True))
            categories2 = set(anime2.genre.values_list("name", flat=True))
            if not categories1 or not categories2:
                return 0
            return fuzz.ratio(" ".join(categories1), " ".join(categories2))

        for anime in all_anime:
            title_similarity = fuzz.ratio(current_anime.title, anime.title)
            category_similarity = average_category_similarity(current_anime, anime)

            if title_similarity > 50 or category_similarity > 50:
                might_like.append((anime, title_similarity, category_similarity))

        might_like.sort(key=lambda x: (-x[1], -x[2]))

        return [anime for anime, _, _ in might_like[:5]] or Anime.objects.order_by("?")[
            :5
        ]

    def get(self, request, pk, *args, **kwargs):
        anime = get_object_or_404(Anime, pk=pk)
        form = AnimeCommentForm()
        user_comment = (
            AnimeComment.objects.filter(anime=anime, user=request.user).first()
            if request.user.is_authenticated
            else None
        )
        profile = (
            UserProfile.objects.get(user=request.user)
            if request.user.is_authenticated
            else None
        )
        user_rating = (
            AnimeRating.objects.filter(anime=anime, user=request.user).first()
            if request.user.is_authenticated
            else None
        )
        is_favorited = (
            AnimeFavorites.objects.filter(anime=anime, user=request.user).exists()
            if request.user.is_authenticated
            else False
        )

        comments_list = AnimeComment.objects.filter(anime=anime).order_by("-created_at")
        paginator = Paginator(comments_list, COMMENT_PAGINATION)
        page = request.GET.get("page")

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        might_like = self.get_might_like_anime(anime)
        first_episode = (
            AnimeEpisode.objects.filter(anime=anime)
            .order_by("season", "episode")
            .first()
        )

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "anime/comments_list.html",
                {"comments": comments, "paginator": paginator},
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "anime/details.html",
            {
                "anime": anime,
                "might_like": might_like,
                "user_comment": user_comment,
                "form": form,
                "profile": profile,
                "comments": comments,
                "paginator": paginator,
                "user_rating": user_rating,
                "first_episode": first_episode,
                "is_favorited": is_favorited,
            },
        )

    def post(self, request, pk):
        form = AnimeCommentForm(data=request.POST)
        anime = get_object_or_404(Anime, pk=pk)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.anime = anime
            comment.user = request.user
            comment.save()
            anime.update_comment()

        return redirect("anime:details", pk=pk)

    def delete(self, request, pk):
        anime = get_object_or_404(Anime, pk=pk)
        comment = get_object_or_404(AnimeComment, anime=anime, user=request.user)
        comment.delete()
        anime.update_comment()

        comments_list = AnimeComment.objects.filter(anime=anime).order_by("-created_at")
        paginator = Paginator(comments_list, COMMENT_PAGINATION)
        page = request.GET.get("page")

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        might_like = self.get_might_like_anime(anime)
        first_episode = (
            AnimeEpisode.objects.filter(anime=anime)
            .order_by("season", "episode")
            .first()
        )

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "anime/comments_list.html",
                {"comments": comments, "paginator": paginator},
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "anime/details.html",
            {
                "anime": anime,
                "might_like": might_like,
                "form": AnimeCommentForm(),
                "user_comment": None,
                "comments": comments,
                "paginator": paginator,
                "first_episode": first_episode,
            },
        )


class WatchView(APIView):
    """
    get:
    Возвращает страницу с данными для просмотра аниме

    post:
    Создает комментарий пользователя

    delete:
    Удаляет комментарий пользователя
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk, current, *args, **kwargs):
        anime_view_count = AnimeViewCount.objects.get(anime=pk)
        episode_cookie_name = f"viewed_{pk}"

        if not request.COOKIES.get(episode_cookie_name):
            anime_view_count.increment_views()

        anime = get_object_or_404(Anime, pk=pk)
        form = AnimeCommentForm()
        user_comment = (
            AnimeComment.objects.filter(anime=anime, user=request.user).first()
            if request.user.is_authenticated
            else None
        )
        profile = (
            UserProfile.objects.get(user=request.user)
            if request.user.is_authenticated
            else None
        )

        comments_list = AnimeComment.objects.filter(anime=anime).order_by("-created_at")
        paginator = Paginator(comments_list, COMMENT_PAGINATION)
        page = request.GET.get("page")

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        seasons = (
            AnimeEpisode.objects.filter(anime=anime)
            .values("season")
            .annotate(episode_count=Count("id"))
            .order_by("season")
        )
        episodes_by_season = {
            season["season"]: AnimeEpisode.objects.filter(
                anime=anime, season=season["season"]
            ).order_by("episode")
            for season in seasons
        }
        current_episode = AnimeEpisode.objects.filter(pk=current, anime=anime).first()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "anime/comments_list.html",
                {"comments": comments, "paginator": paginator},
            )
            return JsonResponse({"html": html})
    
        response = render(
            request,
            "anime/anime_watching.html",
            {
                "anime": anime,
                "user_comment": user_comment,
                "form": form,
                "profile": profile,
                "comments": comments,
                "paginator": paginator,
                "seasons": seasons,
                "episodes_by_season": episodes_by_season,
                "current_episode": current_episode,
            },
        )

        if not request.COOKIES.get(episode_cookie_name):
            expires = datetime.now() + timedelta(days=1)
            response.set_cookie(
                episode_cookie_name,
                "true",
                expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
            )

        return response

    def post(self, request, pk, current):
        form = AnimeCommentForm(data=request.POST)
        anime = get_object_or_404(Anime, pk=pk)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.anime = anime
            comment.user = request.user
            comment.save()
            anime.update_comment()

        return redirect("anime:watch", pk=pk, current=current)

    def delete(self, request, pk, current):
        anime = get_object_or_404(Anime, pk=pk)
        comment = get_object_or_404(AnimeComment, anime=anime, user=request.user)
        comment.delete()
        anime.update_comment()

        comments_list = AnimeComment.objects.filter(anime=anime).order_by("-created_at")
        paginator = Paginator(comments_list, COMMENT_PAGINATION)
        page = request.GET.get("page")

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        seasons = (
            AnimeEpisode.objects.filter(anime=anime)
            .values("season")
            .annotate(episode_count=Count("id"))
            .order_by("season")
        )
        episodes_by_season = {
            season["season"]: AnimeEpisode.objects.filter(
                anime=anime, season=season["season"]
            ).order_by("episode")
            for season in seasons
        }
        current_episode = AnimeEpisode.objects.filter(pk=current, anime=anime).first()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "anime/comments_list.html",
                {"comments": comments, "paginator": paginator},
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "anime/anime_watching.html",
            {
                "anime": anime,
                "form": AnimeCommentForm(),
                "user_comment": None,
                "comments": comments,
                "paginator": paginator,
                "seasons": seasons,
                "episodes_by_season": episodes_by_season,
                "current_episode": current_episode,
            },
        )


class RateView(APIView):
    """
    post:
    Добавляет оценку пользователя

    delete:
    Удаляет оценку пользователя
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, rate, *args, **kwargs):
        anime = get_object_or_404(Anime, pk=pk)

        try:
            rate = int(rate)
        except ValueError:
            return Response(
                {"error": "Invalid rating value"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not rate:
            return Response(
                {"error": "Rating value is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        existing_rating = AnimeRating.objects.filter(anime=anime, user=user).first()

        if existing_rating:
            return Response(
                {"error": "You have already rated this anime"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        AnimeRating.objects.create(anime=anime, user=user, rating=rate)
        anime.update_rating()

        return JsonResponse({"success": True})

    def delete(self, request, rateid, *args, **kwargs):
        with transaction.atomic():
            rating = get_object_or_404(AnimeRating, id=rateid, user=request.user)
            anime = rating.anime
            rating.delete()
            anime.update_rating()
        return JsonResponse({"success": True})


class FavoriteView(APIView):
    """
    post:
    Меняет статус избранного у конкретного аниме от конкретного пользователя
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        try:
            anime = Anime.objects.get(pk=pk)
        except Anime.DoesNotExist:
            return JsonResponse({"success": False}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get("action")

        if action == "add":
            AnimeFavorites.objects.get_or_create(anime=anime, user=user)
            success = True
        elif action == "remove":
            AnimeFavorites.objects.filter(anime=anime, user=user).delete()
            success = True
        else:
            return JsonResponse({"success": False}, status=status.HTTP_400_BAD_REQUEST)

        is_favorited = AnimeFavorites.objects.filter(anime=anime, user=user).exists()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "anime/favorite.html", {"is_favorited": is_favorited}
            )
            return JsonResponse({"success": success, "html": html})

        return JsonResponse({"success": success})
