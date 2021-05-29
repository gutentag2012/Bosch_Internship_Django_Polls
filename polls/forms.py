from django import forms
from .models import Poll
from datetime import date


class PollForm(forms.ModelForm):
    """Form responsible for creating new Polls."""

    # Hidden input to store the relation to the creating user -> User taking from request
    creator = forms.HiddenInput()

    # The start date of the poll by default the current date
    # The default format from the frontend timepicker is applied
    start_date = forms.DateField(
        initial=date.today(),
        input_formats=("%b %d, %Y",),
        widget=forms.DateInput(
            format="%b %d, %Y",
            attrs={
                "class": "datepicker"
            }
        ))

    # The end date of the poll, when no date is suppolied the poll will last forever
    # The default format from the frontend timepicker is applied
    end_date = forms.DateField(
        input_formats=("%b %d, %Y",),
        required=False,
        widget=forms.DateInput(
            format="%b %d, %Y",
            attrs={
                "class": "datepicker"
            }
        ))

    # The first initial three answers are set here and required -> A poll without answers makes no sense
    answer_1 = forms.CharField()
    answer_2 = forms.CharField()
    answer_3 = forms.CharField()

    class Meta:
        """Required class to represent what fields from the model are saved."""
        model = Poll
        fields = [
            "creator",
            "question",
            "start_date",
            "end_date",
        ]

    def clean_end_date(self):
        """Validation method for assuring that the start is before the end date."""
        end_date = self.cleaned_data["end_date"]

        if not end_date:
            return None

        if end_date <= self.cleaned_data["start_date"]:
            raise forms.ValidationError("The end date must be after the start date!")

        return end_date

    def save(self, commit=True):
        """Saving method is overriden, so that the additional poll answer fields can be posted."""
        poll = super(PollForm, self).save(commit=commit)

        # Adds the additional answers to the answers of the poll
        poll.pollanswer_set.create(answer=self.cleaned_data["answer_1"])
        poll.pollanswer_set.create(answer=self.cleaned_data["answer_2"])
        poll.pollanswer_set.create(answer=self.cleaned_data["answer_3"])

        return poll
