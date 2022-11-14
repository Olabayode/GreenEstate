from django.contrib import admin
from django.forms import Textarea
from .models import Admin, NewUser, Security, Resident, Visitor
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = (
        "username",
        "email",
        "usertype",
    )
    list_filter = ("username", "email", "usertype", "is_active", "is_staff")
    list_display = ("username", "email", "usertype", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "email", "usertype")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    formfield_overrides = {
        NewUser: {"widget": Textarea(attrs={"rows": 10, "cols": 40})},
    }
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "usertype",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


# Register your models here.
admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Resident)
admin.site.register(Security)
admin.site.register(Visitor)
admin.site.register(Admin)

