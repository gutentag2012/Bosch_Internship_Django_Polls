from django.contrib import admin
from .models import Poll, PollAnswer, Tag


class AnswerInline(admin.StackedInline):
    model = PollAnswer
    extra = 2


class TagInline(admin.TabularInline):
    model = Tag.polls.through
    extra = 1


class PollAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, TagInline]


admin.site.register(Tag)
admin.site.register(PollAnswer)
admin.site.register(Poll, PollAdmin)
