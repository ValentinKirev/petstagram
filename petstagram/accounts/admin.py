from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(auth_admin.UserAdmin):

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username", "password"
                )
            }),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "profile_picture",
                    "gender"
                )
            }),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }),
        (
            "Important dates",
            {
                "fields": (
                    "last_login", "date_joined"
                )
            }),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username", "password1", "password2", "email"
                )
            }),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "profile_picture",
                    "gender"
                )
            }),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }),
        (
            "Important dates",
            {
                "fields": (
                    "last_login", "date_joined"
                )
            }),
    )
