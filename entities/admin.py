from django.contrib import admin
from .models import Poll, PollAnswer, Tag

# Register your models here.
admin.site.register(Poll)
admin.site.register(PollAnswer)
admin.site.register(Tag)
