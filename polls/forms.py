from django import forms
from .models import Poll, Tag
from datetime import date


class PollForm(forms.ModelForm):
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

    class Meta:
        model = Poll
        fields = [
            "question",
            "start_date",
            "end_date",
        ]
