from django.contrib import admin
from .models import Poll, PollAnswer, Tag


class AnswerInline(admin.TabularInline):
    """Creates an inline version of a PollAnswer for the admin panel"""
    model = PollAnswer
    extra = 1


class TagInline(admin.TabularInline):
    """Creates an inline version of the Tags for the admin panel"""
    model = Tag.polls.through
    extra = 1


class PollAdmin(admin.ModelAdmin):
    """Constructs the displayed version of a Poll for the admin pannel"""
    inlines = [AnswerInline, TagInline]
    list_display = ('question', 'creator', 'count_votes', 'is_still_available', 'start_date', 'end_date')


class AnswerAdmin(admin.ModelAdmin):
    """Constructs the displayed version of a PollAnswer for the admin pannel"""
    list_display = ('answer', 'count_votes', 'poll')


# Registers the models to be edited through the admin panel
admin.site.register(Tag)
admin.site.register(PollAnswer, AnswerAdmin)
admin.site.register(Poll, PollAdmin)
