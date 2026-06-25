from django.db import models


class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('data_request', 'Data Request'),
        ('general', 'General Feedback'),
        ('map_issue', 'Map Issue'),
        ('bug_report', 'Bug Report'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=100, blank=True, default='Anonymous')
    email = models.EmailField(blank=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, default='', help_text='Internal notes about this feedback and actions taken')
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['-submitted_at']
        app_label = 'my_geonode'

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

    def get_category_display_icon(self):
        icons = {
            'data_request': '📊',
            'general': '💬',
            'map_issue': '🗺️',
            'bug_report': '🐛',
        }
        return icons.get(self.category, '📝')
