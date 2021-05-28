from django.contrib import admin
from .models import Poll, PollAnswer, Tag


class AnswerInline(admin.TabularInline):
    model = PollAnswer
    extra = 1


class TagInline(admin.TabularInline):
    model = Tag.polls.through
    extra = 1


class PollAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, TagInline]
    list_display = ('question', 'creator', 'count_votes', 'is_still_available', 'start_date', 'end_date')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'count_votes', 'poll')


admin.site.register(Tag)
admin.site.register(PollAnswer, AnswerAdmin)
admin.site.register(Poll, PollAdmin)
