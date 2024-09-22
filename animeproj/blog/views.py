from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import BlogPost, BlogComment
from .forms import BlogCommentForm

from user.models import UserProfile


COMMENT_PAGINATION = 6


def paginate_comments(request, blog_id):
    comments_list = BlogComment.objects.filter(blog=blog_id).order_by("-created_at")
    paginator = Paginator(comments_list, COMMENT_PAGINATION)
    page = request.GET.get("page")

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return comments, paginator


def render_comments_ajax(request, comments, paginator):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "anime/comments_list.html",
            {
                "comments": comments,
                "paginator": paginator,
            },
        )
        return JsonResponse({"html": html})
    return None


def get_user_profile(request):
    return (
        UserProfile.objects.get(user=request.user)
        if request.user.is_authenticated
        else None
    )


class IndexView(APIView):
    """
    get:
    Возвращает список блогов
    """

    def get(self, request):
        latest_blogs = BlogPost.objects.order_by("-created_at")[:12]
        return render(request, "blog/blog.html", context={"latest_blogs": latest_blogs})


class BlogView(APIView):
    """
    get:
    Возвращает детали блога

    post:
    Создает комментарий пользователя

    delete:
    Удаляет комментарий пользователя
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        profile = get_user_profile(request)
        content_blocks = blog_post.content_blocks.all()
        user_comment = (
            BlogComment.objects.filter(blog=pk, user=request.user).first()
            if request.user.is_authenticated
            else None
        )
        form = BlogCommentForm()

        comments, paginator = paginate_comments(request, pk)
        ajax_response = render_comments_ajax(request, comments, paginator)
        if ajax_response:
            return ajax_response

        return render(
            request,
            "blog/blog_details.html",
            context={
                "blog_post": blog_post,
                "content_blocks": content_blocks,
                "form": form,
                "profile": profile,
                "comments": comments,
                "paginator": paginator,
                "user_comment": user_comment,
            },
        )

    def post(self, request, pk):
        form = BlogCommentForm(data=request.POST)
        blog = get_object_or_404(BlogPost, pk=pk)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()

        return redirect("blog:blog_details", pk=pk)

    def delete(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        profile = get_user_profile(request)

        # Удаление комментария пользователя
        comment = get_object_or_404(BlogComment, blog=pk, user=request.user)
        comment.delete()

        comments, paginator = paginate_comments(request, pk)
        ajax_response = render_comments_ajax(request, comments, paginator)
        if ajax_response:
            return ajax_response

        return render(
            request,
            "blog/blog_details.html",
            {
                "form": BlogCommentForm(),
                "user_comment": None,
                "profile": profile,
                "blog_post": blog_post,
                "content_blocks": blog_post.content_blocks.all(),
                "comments": comments,
                "paginator": paginator,
            },
        )
