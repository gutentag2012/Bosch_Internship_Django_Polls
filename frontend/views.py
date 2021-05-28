from django.shortcuts import render
from django.http import Http404
from entities.models import Poll


def get_object_or_404(holder, pk):
    try:
        element = holder.objects.get(pk=pk)
    except holder.DoesNotExist:
        raise Http404("Poll does not exist!")
    return element


def log_in_view(request):
    return render(request, "login.html", {})


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
    error = None

    if not request.user.is_authenticated:
        vote = None
        error = "You need to log in in order to vote!"

    print(error)

    poll = get_object_or_404(Poll, pk=poll_id)
    poll_answer = poll.pollanswer_set.filter(users__id=request.user.id)
    print(poll_answer)

    context = {
        "poll": {
            "question": poll.question,
            "username": poll.user.username,
            "tags": poll.get_tags(),
            "start_date": poll.start_date.strftime('%d.%m.%Y'),
            "votes": poll.count_votes() if vote else 0,
            "answers": []
        },
        "not_voted": False if vote else True,
        "is_error": True if error else False,
        "msg_error": error
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
