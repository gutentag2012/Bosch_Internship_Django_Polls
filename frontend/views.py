from django.shortcuts import render
from entities.models import Poll


def home_page_view(request):
    poll_objs = Poll.objects.all()
    polls = []
    for i, item in enumerate(poll_objs):
        answer_objs = item.pollanswer_set.all()
        votes = 0
        for answer in answer_objs:
            votes += answer.users.all().count()

        tag_objs = item.tag_set.all()
        tags = []

        for tag in tag_objs:
            tags.append({
                "name": tag.name,
                "color": tag.color % 15 + 1
            })

        polls.append({
            "color_index": i % 15 + 1,
            "question": item.question,
            "tags": tags,
            "votes": votes
        })
    return render(request, "home.html", {"polls": polls})
