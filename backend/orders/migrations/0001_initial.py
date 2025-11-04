from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("product_url", models.URLField(max_length=1000)),
                ("status", models.CharField(choices=[("queued", "Queued"), ("running", "Running"), ("success", "Success"), ("failed", "Failed")], default="queued", max_length=20)),
                ("error_message", models.TextField(blank=True)),
                ("logs", models.JSONField(blank=True, null=True)),
                ("logs_text", models.TextField(blank=True)),
            ],
        ),
    ]



