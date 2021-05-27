from django.shortcuts import render
from entities.models import Poll


def home_page_view(request):
    search_term = request.GET.get("search") or ""
    print(search_term)
    poll_objs = Poll.objects.filter(question__icontains=search_term)
    context = {"polls": [], "search_term": search_term}

    for i, item in enumerate(poll_objs):
        context["polls"].append({
            "color_index": i % 15 + 1,
            "question": item.question,
            "tags": item.get_tags(),
            "votes": item.count_votes()
        })

    return render(request, "home.html", context)
