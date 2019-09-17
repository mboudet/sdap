from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from sdap.users.forms import UserChangeForm, UserCreationForm
from sdap.users.models import Notification

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": [("name",), ("last_name",), ("institut",),]}),)
    list_display = ["username", "name", "last_name", "institut", "is_superuser"]
    search_fields = ["name"]

class NotificationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Notification, NotificationAdmin)
