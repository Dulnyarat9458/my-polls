from django.contrib import admin

from my_polls.votes.models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'choice', 'created_at')
    search_fields = ('user__username', 'choice__choice_text')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False
