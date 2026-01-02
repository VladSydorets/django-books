from django.contrib import admin

from .models import WaitlistApplication


@admin.register(WaitlistApplication)
class WaitlistApplicationAdmin(admin.ModelAdmin):
    list_display = ("email", "is_confirmed", "created_at")
    search_fields = ("email",)
    list_filter = ("is_confirmed", "created_at")
    ordering = ("-created_at",)
