
from django.contrib import admin
from .feedback import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'category', 'status', 'submitted_at']
    list_filter = ['category', 'status', 'submitted_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['submitted_at', 'ip_address']
    ordering = ['-submitted_at']
    list_per_page = 25
