from django.contrib import admin

from .models import AttendanceBook


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'period', 'place', 'check')
    list_filter = ('user', 'date', 'period', 'place', 'check')
    exclude = []

    fieldsets = (
        (None, {'fields': ('user', 'date', 'period', 'place', 'check')}),
    )
    add_fieldsets = (
        (None, {'fields': ('user', 'date', 'period', 'place', 'check')}),
    )

admin.site.register(AttendanceBook)