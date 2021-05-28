from django.contrib import admin
from .models import Poll, PollAnswer, Tag

admin.site.register(Poll)
admin.site.register(PollAnswer)
admin.site.register(Tag)
