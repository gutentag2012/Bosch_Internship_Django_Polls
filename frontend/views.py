from django.shortcuts import render
from entities.models import Poll
import datetime


def home_page_view(request):
    search_term = request.GET.get("search") or ""
    poll_objs = Poll.objects.filter(question__icontains=search_term)

    context = {"polls": [], "search_term": search_term}

    for i, item in enumerate(poll_objs):
        context["polls"].append({
            "id": item.id,
            "color_index": i % 15 + 1,
            "question": item.question,
            "tags": item.get_tags(),
            "votes": item.count_votes()
        })

    return render(request, "overview_polls.html", context)


def single_poll_view(request, poll_id):
    vote = request.POST.get("vote")

    poll = Poll.objects.get(id=poll_id)
    context = {
        "poll": {
            "question": poll.question,
            "username": poll.user.username,
            "start_date": poll.start_date.strftime('%d.%m.%Y'),
            "votes": poll.count_votes() if vote else 0,
            "answers": []
        },
        "voted": True if vote else False,
    }

    i = 0
    for answer in poll.pollanswer_set.all():
        context["poll"]["answers"].append({
            "id": answer.id,
            "content": answer.answer,
            "color_index": i % 15 + 1,
            "votes_percent": (answer.count_votes() * 100 / context["poll"]["votes"]) if vote else 0,
            "votes": answer.count_votes() if vote else 0,
            "is_voted": int(answer.id) == int(vote) if vote else False,
        })
        i += 1

    return render(request, "single_poll.html", context)
