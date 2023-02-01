from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Person, User, Family


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["email", "is_active"]
    list_filter = ["groups", "is_active"]
    readonly_fields = ["date_joined", "last_login"]
    search_fields = [
        "email",
        "person__first_name",
        "person__last_name",
        "person__family__family_name",
    ]
    ordering = ["-id"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        (
            None,
            {
                "fields": ("email", "person", "password"),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Info",
            {
                "fields": (
                    "date_joined",
                    "last_login",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ["family_name"]
    search_fields = ["family_name"]
