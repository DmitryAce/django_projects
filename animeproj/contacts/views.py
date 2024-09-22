from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string

from .forms import ConversationMessageForm
from .models import Conversation, ConversationMessage


CONTACTS_PAGINATION = 6
MESSAGES_PAGINATION = 6


class IndexView(APIView):
    """
    get:
    Возвращает данные для страницы контактов
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        contacts = Conversation.objects.filter(members=request.user)
        paginator = Paginator(contacts, CONTACTS_PAGINATION)
        page = request.GET.get("page")

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "contacts/contacts_list.html",
                {"contacts": contacts, "paginator": paginator, "request": request},
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "contacts/contacts.html",
            context={"contacts": contacts, "paginator": paginator, "request": request},
        )


class NewView(APIView):
    """
    get:
    Возвращает форму для написания сообщения пользователю

    post:
    Создает сообщение пользователя и инициирует диалог
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        form = ConversationMessageForm()
        return render(request, "contacts/new.html", context={"form": form})

    def post(self, request, pk):
        recipient = get_object_or_404(User, pk=pk)

        conversation = (
            Conversation.objects.filter(members=request.user)
            .filter(members=recipient)
            .first()
        )

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.members.add(request.user, recipient)
            conversation.save()

        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.user = request.user
            message.save()

            conversation.modified_at = timezone.now()
            conversation.save()

            return redirect("contacts:conversation", pk=conversation.pk)

        return render(request, "contacts/new.html", context={"form": form})


class ConversationView(APIView):
    """
    get:
    Взвращает данные для диалога пользователя

    post:
    Создает сооьщение пользователя
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        recipient = conversation.members.exclude(pk=request.user.pk).first()
        messages = ConversationMessage.objects.filter(conversation_id=pk).order_by(
            "-created_at"
        )
        form = ConversationMessageForm()

        paginator = Paginator(messages, MESSAGES_PAGINATION)
        page = request.GET.get("page")

        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages = paginator.page(1)
        except EmptyPage:
            messages = paginator.page(paginator.num_pages)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "contacts/details_list.html",
                {
                    "messages": messages,
                    "request": request,
                },
            )
            return JsonResponse({"html": html})

        return render(
            request,
            "contacts/details.html",
            context={
                "messages": messages,
                "form": form,
                "recipient": recipient,
                "conversation": conversation,
                "request": request,
            },
        )

    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        recipient = conversation.members.exclude(pk=request.user.pk).first()

        if not recipient:
            return JsonResponse(
                {"success": False, "error": "Recipient not found."}, status=404
            )

        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.user = request.user
            message.save()

            conversation.modified_at = timezone.now()
            conversation.save()

            page = request.POST.get("page", 1)
            paginator = Paginator(
                ConversationMessage.objects.filter(conversation=conversation).order_by(
                    "-created_at"
                ),
                MESSAGES_PAGINATION,
            )

            try:
                messages = paginator.page(page)
            except PageNotAnInteger:
                messages = paginator.page(1)
            except EmptyPage:
                messages = paginator.page(paginator.num_pages)

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "contacts/details_list.html",
                    {
                        "messages": messages,
                        "recipient": recipient,
                        "paginator": paginator,
                        "request": request,
                    },
                )
                return JsonResponse({"success": True, "html": html})

            return redirect("contacts:conversation", pk=pk)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors})

        return render(request, "contacts/new.html", context={"form": form})
