from django.contrib import admin
from my_polls.polls.models import Poll, Choice
# Register your models here.


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'created_at')
    search_fields = ('question',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice_text')
    search_fields = ('choice_text',)
    list_filter = ('poll',)
    
    def has_add_permission(self, request):
        return False
