from __future__ import annotations

from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New: support multiple product URLs in one order
    product_urls = models.JSONField(null=True, blank=True)
    # Optional clothing size to select on product pages
    size = models.CharField(max_length=50, default="Medium")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    error_message = models.TextField(blank=True)

    # Logs from Browser Use run; stored as JSON if possible
    logs = models.JSONField(null=True, blank=True)
    # Fallback/raw text representation
    logs_text = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - admin readability
        return f"Order #{self.pk} - {self.status}"


