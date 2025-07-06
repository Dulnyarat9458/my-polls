from django.contrib import admin
from my_polls.polls.models import Poll, Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'user', 'created_at')
    search_fields = ('question',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll', 'choice_text', 'user')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('poll__user')

    def user(self, obj):
        return obj.poll.user
