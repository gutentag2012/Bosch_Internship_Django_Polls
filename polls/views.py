from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import PollForm
from .models import Poll, Tag
from datetime import datetime


def log_in_view(request):
    """The view that is responsible for logging the users in. Also performs a logout on the current user."""
    context = {}

    logout(request)

    if request.method == "POST":
        # Authenticates with the form in the frontend
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password"))

        if user is None:
            # The given data was invalid, so display an error message
            context["is_error"] = True
            context["msg_error"] = "Invalid username or password!"
        else:
            # If the user could be authenticated, he is logged in and redirected to the homepage
            login(request, user)
            return redirect("home")

    return render(request, "login.html", context)


def sign_up_view(request):
    """The view that is responsible creating a new user."""
    context = {}

    # Create default form for GET requests
    form = UserCreationForm()

    if request.method == "POST":
        # Create form for POST requests
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database if the form is valid
            form.save()

            # Log the new user into the system
            form_data = form.cleaned_data
            user = authenticate(
                username=form_data.get("username"),
                password=form_data.get("password1"))
            login(request, user)

            return redirect("home")

    # Set the form for the context
    context["form"] = form

    return render(request, "signup.html", context)


def home_page_view(request):
    """The view that displays all available polls and filters them according to the user input."""

    # Retrieves the search term from the request or a default empty string
    search_term = request.GET.get("search") or ""

    # Filters the poll objects after the search term and whether they are available or not (Search respects both the name and the tags)
    poll_objs = Poll.objects.filter(Q(question__icontains=search_term) | Q(tag__name__icontains=search_term)).distinct()
    poll_objs = filter(lambda e: e.is_still_available(), poll_objs)

    # Builds the context with a list of polls and the search term
    context = {"polls": [], "search_term": search_term}

    # Extracts the important information out of the poll objects and adds them to the context
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
    """The view that displays a poll with is answers. It also handles the voting interaction."""

    # Retrieves a possible vote from the request
    vote = request.POST.get("vote")

    # Get the poll for this request and the answer of the user (if there is one in the database)
    poll = get_object_or_404(Poll, pk=poll_id)
    user_answer = poll.pollanswer_set.filter(user_votes__id=request.user.id).first()

    # Creates the inital context
    context = {
        "poll": {
            "question": poll.question,
            "username": poll.creator.username,
            "tags": poll.get_tags(),
            "start_date": poll.start_date.strftime('%d.%m.%Y'),
            "answers": []
        },
        "is_error": False,
        "msg_error": ""
    }

    if not request.user.is_authenticated:
        # If the user is not authenticated he is not able to vote and an error message is displayed
        context["msg_error"] = "You need to log in in order to vote!"
        context["is_error"] = True
        # If the user made a vote it is voided here
        vote = None
    else:
        # If the user is authenticated to the following:
        if user_answer is not None:
            # If there was a vote in the database add it to the view context
            vote = user_answer.id
        elif vote is not None:
            # Add the vote to the database
            poll.pollanswer_set.get(pk=vote).user_votes.add(request.user)

    # If there is a vote a boolean is entered into the context and the number of votes
    context["voted"] = True if vote else False
    context["poll"]["votes"] = poll.count_votes() if vote else 0

    # Fills the answers inside of the context with the important information
    i = 0
    for answer in poll.pollanswer_set.all():
        context["poll"]["answers"].append({
            "id": answer.id,
            "content": answer.answer,
            "color_index": i % 15 + 1,
            "votes_percent": (answer.count_votes() * 100 / context["poll"]["votes"]) if context["poll"][
                                                                                            "votes"] > 0 else 0,
            "votes": answer.count_votes() if vote else 0,
            "is_voted": int(answer.id) == int(vote) if vote else False,
        })
        i += 1

    return render(request, "single_poll.html", context)


def create_poll_view(request):
    context = {}
    form = PollForm()
    context["form"] = form

    context["tags"] = []
    for tag in request.POST:
        if tag.startswith("chip"):
            context["tags"].append({"tag": request.POST.get(tag)})

    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            start_date = datetime.strptime(request.POST.get("start_date"), "%b %d, %Y").date()
            end_date = None
            if request.POST.get("end_date"):
                end_date = datetime.strptime(request.POST.get("end_date"), "%b %d, %Y").date()
            var = Poll.objects.create(**{
                "creator": request.user,
                "question": request.POST.get("question"),
                "start_date": start_date,
                "end_date": end_date,
            })
            for tag in context["tags"]:
                tag_to_add = None
                try:
                    tag_to_add = Tag.objects.get(name=tag["tag"])
                except Tag.DoesNotExist:
                    tag_to_add = Tag.objects.create(**{
                        "name": tag["tag"],
                        "color": Tag.objects.all().count()
                    })
                var.tag_set.add(tag_to_add)
            return redirect("home")


    return render(request, "create_poll.html", context)
