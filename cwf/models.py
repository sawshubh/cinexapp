import json
from urllib.parse import quote

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.mail import send_mail

try:
    from django.db.models import JSONField
except:
    from django.contrib.postgres.fields import JSONField


# Create your models here.
class MyManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class checkpoint(models.Model):
    cp_type = models.CharField(unique=True, default="", max_length=50)
    serial_no = models.IntegerField(db_index=True, default=1)
    cp_details = JSONField()
    checkpoint_other_details = models.TextField(default="{}")
    last_modified_on = models.DateTimeField(db_index=True, auto_now=True)
    objects = MyManager()

    class Meta:
        db_table = "checkpoint"
        verbose_name = "Checkpoint"
        verbose_name_plural = "Checkpoints"

    def __str__(self):
        return self.cp_type


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user_rec = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user_rec.set_password(password)
        user_rec.save(using=self._db)
        return user_rec

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """

    user_id = models.CharField(_("user id"), max_length=254, unique=True)
    first_name = models.CharField(_("first name"), max_length=254)
    last_name = models.CharField(_("last name"), max_length=254)
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    login_type = models.CharField(_("login type"), default="social", max_length=254)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    other_details = JSONField(default=dict)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    gmail_page_token = models.CharField(
        _("Gmail Page Token"), default="", max_length=254
    )
    last_modified_on = models.DateTimeField(db_index=True, auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("customuser")
        verbose_name_plural = _("customusers")

    def get_absolute_url(self):
        # return "/users/%s/" % urlquote(self.email)
        return "/users/%s/" % quote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
