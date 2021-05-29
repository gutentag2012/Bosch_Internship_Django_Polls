from django import forms
from .models import Poll
from datetime import date


class PollForm(forms.ModelForm):
    creator = forms.HiddenInput()

    start_date = forms.DateField(
        initial=date.today(),
        input_formats=("%b %d, %Y",),
        widget=forms.DateInput(
            format="%b %d, %Y",
            attrs={
                "class": "datepicker"
            }
        ))

    end_date = forms.DateField(
        input_formats=("%b %d, %Y",),
        required=False,
        widget=forms.DateInput(
            format="%b %d, %Y",
            attrs={
                "class": "datepicker"
            }
        ))

    answer_1 = forms.CharField()
    answer_2 = forms.CharField()
    answer_3 = forms.CharField()

    class Meta:
        model = Poll
        fields = [
            "creator",
            "question",
            "start_date",
            "end_date",
        ]

    def clean_end_date(self):
        end_date = self.cleaned_data["end_date"]
        if not end_date:
            return None
        if end_date <= self.cleaned_data["start_date"]:
            raise forms.ValidationError("The end date must be after the start date!")
        return end_date

    def save(self, commit=True):
        poll = super(PollForm, self).save(commit=commit)
        poll.pollanswer_set.create(answer=self.cleaned_data["answer_1"])
        poll.pollanswer_set.create(answer=self.cleaned_data["answer_2"])
        poll.pollanswer_set.create(answer=self.cleaned_data["answer_3"])
        return poll
