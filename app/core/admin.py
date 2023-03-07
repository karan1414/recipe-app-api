from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):  #or inherit from (admin.Model) if do not want to change fieldsets
    """ Define the admin page for users """
    # how to order records in admin view
    ordering = ['id']
    # what all fields to show in admin view
    list_display = ["email", "name"]
    # show only fields that we created ourself in our models or was available in permissions mixin
    fieldsets = (
        # section without title since none 
        (None, {'fields': ('email', 'password')}),
        (
            _("Permissions"), 
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            }
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]

# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredients)