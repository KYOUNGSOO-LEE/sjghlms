from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import MyUser
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'name', 'is_student', 'is_teacher', 'is_coordinator', 'year_admission', 'user_code')
    list_filter = ('is_student', 'is_teacher', 'is_coordinator', 'year_admission',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'year_admission', 'user_code')}),
        ('Permissions', {'fields': ('is_student', 'is_teacher', 'is_coordinator',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('name', 'year_admission', 'user_code')}),
        ('Permissions', {'fields': ('is_student', 'is_teacher', 'is_coordinator',)}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)