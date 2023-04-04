from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_email(value):
    if "vit.ac.in" in value:
        return value
    else:
        return ValidationError("Only VIT emails allowed.")

def validate_tenure(value):
    if value.is_digit() and int(value) > 2022 and int(value) < 250:
        return value
    else:
        return ValidationError("Please enter a valid tenure.")


class User(AbstractUser):
    """
    Default custom user model for Student Welfare Backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=False, max_length=255)
    email = models.EmailField(_("Email of User"), max_length=254, validators=[validate_email])
    phone_no = models.CharField(_("Phone number of User"), blank=False, max_length=15)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    tenure = models.CharField(_("Pass out year of the student"), blank=True, max_length=4, validators=[validate_tenure])
    is_faculty = models.BooleanField(_("User is faculty"), default=False)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"Institute id": self.username})
