from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic.edit import DeleteView
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import PollForm
from .models import Poll, Tag, PollAnswer
from datetime import date


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

    # Filters the poll objects after the search term and whether they are available or not
    # (Search respects both the name and the tags)
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
            "id": poll.id,
            "question": poll.question,
            "username": poll.creator.username,
            "tags": poll.get_tags(),
            "start_date": poll.start_date.strftime('%d.%m.%Y'),
            "answers": []
        },
        "is_error": False,
        "msg_error": "",
        "is_creator": request.user == poll.creator
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
            try:
                # Add the vote to the database
                poll.pollanswer_set.get(pk=vote).user_votes.add(request.user)
            except PollAnswer.DoesNotExist:
                # A wrong answer key is posted, the vote is voided
                vote = None

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


def get_json_tags_from_post(request):
    """This helper method maps all chips of tags from a POST request into a list of their values."""
    result = []

    for key in request.POST:
        # If the key inside of the POST request starts with "chip" it is a valid tag-chip
        if key.startswith("chip"):
            # Add the corresponding value to the result
            result.append({"tag": request.POST.get(key)})

    return result


def find_or_create_tag(tag):
    """This helper method takes a tag name and either returns the saved tag in the database
    or if there is none creates a new tag and returns this one."""

    try:
        # Tries to retrieve the tag from the database
        return Tag.objects.get(name=tag)
    except Tag.DoesNotExist:
        # If the tag could not be found, a new one is created
        return Tag.objects.create(
            name=tag,
            color=Tag.objects.all().count()
        )


def for_other_answers_in_poll(request, method):
    """This helper method gets all answers from a POST request with an index greater than 3 and executes a method
    to the polls answers. The index must me greater than 3 because the first three answers are already added."""

    for key in request:
        # If the key does not contain "answer_" then it is no answer and the loop can continue
        if not key.startswith("answer_"):
            continue

        # Split by the underscore to get the right side that represents the index
        index = key.split("_")[1]

        # If the index is smaller or equal to 3 the loop can continue
        if int(index) <= 3:
            continue

        # Execute the method on the current answer
        method(request.get(key), index)


def create_poll_view(request):
    """The view that creates new polls for the system."""

    # Create the starting poll form for the GET request
    form = PollForm(initial={"creator": request.user, "start_date": date.today()})

    # Create the initial context with the form, all tags and the tags from a potential POST request
    context = {
        "form": form,
        "all_tags": [e[0] for e in Tag.objects.values_list("name")],
        "tags": get_json_tags_from_post(request),
        "answers": []
    }

    if request.method == "POST":
        # Saves the form with the posted values in the context
        context["form"] = PollForm(request.POST)

        if context["form"].is_valid():
            # If the form has valid data it is saved together with the first three answers
            poll = context["form"].save()

            # !Important Note: The tags still have to be added afterwards together with possible additional answers
            for tag in context["tags"]:
                # Adds all tags inside of the context to the polls tag set
                poll.tag_set.add(find_or_create_tag(tag["tag"]))

            # Adding all remaining answers form the POST request to the polls answers
            for_other_answers_in_poll(request.POST, lambda answer, key: poll.pollanswer_set.create(answer=answer))

            # Return to the homepage
            return redirect("home")

        # I the form was not valid, the other poll answers (the ones after the first three)
        # still have to be added to the context
        for_other_answers_in_poll(request.POST,
                                  lambda answer, key: context["answers"].append({"answer": answer, "key": key}))

    if not request.user.is_authenticated:
        context["is_error"] = True
        context["msg_error"] = "You need to be logged in in order to create a poll!"

    return render(request, "create_poll.html", context)


class PollDeleteView(DeleteView):
    model = Poll
    template_name = "delete_poll.html"

    def get_success_url(self):
        return reverse("home")

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, kwargs=kwargs)
        else:
            return redirect(".")

    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, kwargs=kwargs)
        else:
            return redirect(".")
