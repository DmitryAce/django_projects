from django.contrib import admin


from .models import Conversation, ConversationMessage


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('display_members', 'created_at', 'modified_at', 'last_message')
    search_fields = ('members__username', )
    list_filter = ('created_at', 'modified_at',)

    def display_members(self, obj):
        return ", ".join([user.username for user in obj.members.all()])
    display_members.short_description = 'Members'
    
    def last_message(self, obj):
        return obj.messages.last().content if obj.messages.exists() else 'No messages'
    last_message.short_description = 'Last Message'


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'user', 'created_at', 'is_read', 'content_preview')
    search_fields = ('conversation__members__username', 'user__username')
    list_filter = ('is_read', 'created_at')

    def content_preview(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_preview.short_description = 'Message Preview'
