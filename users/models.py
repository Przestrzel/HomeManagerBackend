from django.db import models
from typing import Any
from allauth.account.models import EmailAddress
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create(email=email, password=password, **extra_fields)

    def create(self, *args: Any, **kwargs: Any) -> "User":
        if not (email := kwargs.pop("email", None)):
            raise ValueError("Email must be set")
        if not (password := kwargs.pop("password", None)):
            raise ValueError("Password must be set")

        user: User = self.model(email=email, **kwargs)
        user.clean()
        user.set_password(password)
        user.save(using=self._db)

        if "dj_rest_auth.registration" not in settings.INSTALLED_APPS or user.is_superuser:
            EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    person = models.OneToOneField(
        "users.Person", on_delete=models.CASCADE, related_name="user", null=True
    )
    email = models.EmailField(_("Email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []
    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return f"{self.email}"

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def family(self) -> "Family":
        return self.person.family


class Family(models.Model):
    family_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("family")
        verbose_name_plural = _("families")


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    family = models.ManyToManyField(Family)
