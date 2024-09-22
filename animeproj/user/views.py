from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from .forms import UserRegistrationForm, ProfileForm, CustomAuthenticationForm
from .models import UserProfile

from anime.models import AnimeFavorites, Anime

PAGINATION = 8

def paginate_queryset(request, queryset, per_page=PAGINATION):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get("page", 1)

    try:
        paginated_data = paginator.page(page)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    return paginated_data, paginator


class RegisterView(APIView):
    """
    get:
    Возвращает форму для регистрации

    post:
    Регистрирует пользователя
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:index")

        form = UserRegistrationForm()
        return render(request, "user/register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(user=new_user)
            auth_login(request, new_user)

            refresh = RefreshToken.for_user(new_user)
            response = redirect("core:index")
            response.set_cookie(
                settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0].lower() + "-access",
                str(refresh.access_token),
            )
            response.set_cookie(
                settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0].lower() + "-refresh",
                str(refresh),
            )
            return response

        return render(request, "user/register.html", {"form": form})


class LoginView(APIView):
    """
    get:
    Возвращает форму для входа

    post:
    Авторизует пользователя
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:index")
        form = CustomAuthenticationForm()
        return render(request, "user/login.html", {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user:
                auth_login(request, user)
                refresh = RefreshToken.for_user(user)
                response = redirect("core:index")
                response.set_cookie(
                    settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0].lower() + "-access",
                    str(refresh.access_token),
                )
                response.set_cookie(
                    settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0].lower() + "-refresh",
                    str(refresh),
                )
                return response

            form.add_error(None, "Invalid credentials.")

        return render(request, "user/login.html", {"form": form})


class ProfileView(APIView):
    """
    get:
    Возвращает профиль пользователя

    post:
    Обновляет авотарку профиля
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        animes_ids = AnimeFavorites.objects.filter(user=request.user).values_list(
            "anime_id", flat=True
        )
        animes = Anime.objects.filter(id__in=animes_ids)

        animes, paginator = paginate_queryset(request, animes)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "core/general_list.html", {"animes": animes, "paginator": paginator}
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "user/profile.html",
            {
                "user": request.user,
                "profile": profile,
                "form": ProfileForm(instance=profile),
                "animes": animes,
                "paginator": paginator,
            },
        )

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        animes_ids = AnimeFavorites.objects.filter(user=request.user).values_list(
            "anime_id", flat=True
        )
        animes = Anime.objects.filter(id__in=animes_ids)
        animes, paginator = paginate_queryset(request, animes)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "core/general_list.html", {"animes": animes, "paginator": paginator}
            )
            return JsonResponse({"html": html})

        if form.is_valid():
            form.save()

        return render(
            request,
            "user/profile.html",
            {
                "user": request.user,
                "profile": profile,
                "form": form,
                "animes": animes,
                "paginator": paginator,
            },
        )


class ProfileDetailView(APIView):
    """
    get:
    Возвращает профиль другого пользователя
    """

    def get(self, request, user_id):
        profile_user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(UserProfile, user=profile_user)

        animes_ids = AnimeFavorites.objects.filter(user=user_id).values_list(
            "anime_id", flat=True
        )
        animes = Anime.objects.filter(id__in=animes_ids)

        animes, paginator = paginate_queryset(request, animes)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "core/general_list.html", {"animes": animes, "paginator": paginator}
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "user/profile.html",
            {
                "user": profile_user,
                "profile": profile,
                "animes": animes,
                "paginator": paginator,
            },
        )
