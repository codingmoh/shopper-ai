from django.contrib import admin, messages
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django_q.tasks import async_task
from django.utils.safestring import mark_safe
import json

from .models import Order


class OrderAdminForm(forms.ModelForm):
    # Human-friendly textarea: one URL per Zeile
    product_urls_text = forms.CharField(
        label="Produkt-URLs",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Eine URL pro Zeile"}),
        help_text=(
            "Gib mehrere Produkt-URLs zeilenweise ein. Die erste URL wird auch im Feld "
            "'product_url' gespeichert (für Abwärtskompatibilität)."
        ),
    )

    class Meta:
        model = Order
        # Exponiere nicht direkt das JSON-Feld, sondern die Textarea
        exclude = ("product_urls",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Vorbelegen: aus JSON-Liste -> Textarea
        urls = []
        if getattr(self.instance, "product_urls", None):
            try:
                urls = [str(u) for u in (self.instance.product_urls or [])]
            except Exception:
                urls = []
        if urls:
            self.fields["product_urls_text"].initial = "\n".join(urls)

    def clean(self):
        cleaned = super().clean()
        text = cleaned.get("product_urls_text", "") or ""
        # Parse: trim, entferne leere Zeilen
        lines = [l.strip() for l in text.splitlines()]
        urls = [l for l in lines if l]
        if urls:
            validator = URLValidator()
            for u in urls:
                try:
                    validator(u)
                except ValidationError as exc:
                    raise ValidationError({"product_urls_text": f"Ungültige URL: {u}"}) from exc
        cleaned["_parsed_product_urls"] = urls
        return cleaned

    def save(self, commit=True):
        instance: Order = super().save(commit=False)
        urls = self.cleaned_data.get("_parsed_product_urls", [])
        # Setze JSON-Feld konsistent
        instance.product_urls = urls or None
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = ("id", "status", "url_count", "size", "created_at", "updated_at")
    list_filter = ("status", "created_at", "size")
    search_fields = ("id",)
    readonly_fields = ("created_at", "updated_at", "logs_pretty", "logs_text", "error_message")

    fieldsets = (
        (None, {
            "fields": ("status", "size", "product_urls_text"),
            "description": "Gib mehrere Produkt-URLs zeilenweise ein."
        }),
        ("Logs", {"fields": ("error_message", "logs_pretty", "logs_text")}),
        ("Zeitstempel", {"fields": ("created_at", "updated_at")}),
    )

    def url_count(self, obj: Order) -> int:
        try:
            return len(obj.product_urls or [])
        except Exception:
            return 0
    url_count.short_description = "#URLs"

    def logs_pretty(self, obj: Order) -> str:
        try:
            if obj.logs is None:
                return ""
            pretty = json.dumps(obj.logs, ensure_ascii=False, indent=2)
            return mark_safe(f"<pre style='white-space:pre-wrap; word-break:break-word; margin:0'>{pretty}</pre>")
        except Exception:
            return ""
    logs_pretty.short_description = "Logs (JSON)"

    def save_model(self, request, obj, form, change):
        # Save first to ensure we have a primary key
        super().save_model(request, obj, form, change)

        # Only enqueue when created from admin (not on edits)
        if not change:
            if obj.status != Order.Status.QUEUED:
                obj.status = Order.Status.QUEUED
                obj.save(update_fields=["status", "updated_at"])

            try:
                async_task("orders.tasks.process_order", obj.id)
                messages.success(request, "Order wurde in die Queue gestellt.")
            except Exception as exc:  # noqa: BLE001
                messages.warning(
                    request,
                    f"Order gespeichert, aber Queueing fehlgeschlagen: {exc}",
                )


