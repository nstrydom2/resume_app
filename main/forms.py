import time

from django import forms
from django.core import signing
from django.core.exceptions import ValidationError

from .models import ContactProfile
from .services import (
    BUDGET_CHOICES,
    CONTACT_METHOD_CHOICES,
    CONTACT_SERVICE_CHOICES,
)

CONTACT_TOKEN_SALT = "main.contact-form"
CONTACT_TOKEN_MAX_AGE = 60 * 60 * 2
CONTACT_MIN_SECONDS = 2

TEXT_INPUT = {"class": "form-control"}


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={**TEXT_INPUT, "placeholder": "Your full name", "autocomplete": "name"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={**TEXT_INPUT, "placeholder": "you@example.com", "autocomplete": "email"}
        ),
    )
    business_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                **TEXT_INPUT,
                "placeholder": "Business name (optional)",
                "autocomplete": "organization",
            }
        ),
    )
    service = forms.ChoiceField(
        choices=CONTACT_SERVICE_CHOICES,
        required=True,
        widget=forms.Select(attrs=TEXT_INPUT),
    )
    message = forms.CharField(
        max_length=4000,
        required=True,
        label="Description of the problem",
        widget=forms.Textarea(
            attrs={
                **TEXT_INPUT,
                "placeholder": "What is happening now, and what would a good outcome look like?",
                "rows": 6,
            }
        ),
    )
    current_process = forms.CharField(
        max_length=500,
        required=False,
        label="Current process or tools",
        widget=forms.Textarea(
            attrs={
                **TEXT_INPUT,
                "placeholder": "For example: monthly Excel exports, copied into a report by hand.",
                "rows": 3,
            }
        ),
    )
    volume_frequency = forms.CharField(
        max_length=200,
        required=False,
        label="Estimated volume or frequency",
        widget=forms.TextInput(
            attrs={
                **TEXT_INPUT,
                "placeholder": "e.g. 12 files/month, 2,000 rows/week",
            }
        ),
    )
    desired_deadline = forms.CharField(
        max_length=120,
        required=False,
        label="Desired deadline",
        widget=forms.TextInput(
            attrs={**TEXT_INPUT,                 "placeholder": "e.g. end of March, or flexible",}
        ),
    )
    budget_range = forms.ChoiceField(
        choices=BUDGET_CHOICES,
        required=False,
        label="Budget range",
        widget=forms.Select(attrs=TEXT_INPUT),
    )
    preferred_contact = forms.ChoiceField(
        choices=CONTACT_METHOD_CHOICES,
        required=False,
        label="Preferred contact method",
        widget=forms.Select(attrs=TEXT_INPUT),
    )
    company_website = forms.CharField(
        required=False,
        label="Leave this field blank",
        widget=forms.TextInput(
            attrs={
                "class": "hp-field",
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
            }
        ),
    )
    form_token = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = ContactProfile
        fields = (
            "name",
            "email",
            "business_name",
            "service",
            "message",
            "current_process",
            "volume_frequency",
            "desired_deadline",
            "budget_range",
            "preferred_contact",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].choices = [
            ("", "Select the type of help you need")
        ] + CONTACT_SERVICE_CHOICES
        self.fields["form_token"].initial = signing.dumps(
            {"created": time.time()}, salt=CONTACT_TOKEN_SALT
        )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_company_website(self):
        value = self.cleaned_data.get("company_website", "")
        if value:
            raise ValidationError("This field must be left blank.")
        return value

    def clean_form_token(self):
        token = self.cleaned_data.get("form_token")
        try:
            payload = signing.loads(
                token, salt=CONTACT_TOKEN_SALT, max_age=CONTACT_TOKEN_MAX_AGE
            )
        except signing.SignatureExpired:
            raise ValidationError("This form has expired. Please refresh and try again.")
        except signing.BadSignature:
            raise ValidationError(
                "The form could not be verified. Please refresh and try again."
            )

        try:
            created = float(payload["created"])
        except (KeyError, TypeError, ValueError):
            raise ValidationError(
                "The form could not be verified. Please refresh and try again."
            )

        if time.time() - created < CONTACT_MIN_SECONDS:
            raise ValidationError(
                "Please take a moment to complete the form, then submit again."
            )
        return token
