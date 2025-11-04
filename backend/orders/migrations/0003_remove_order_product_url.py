from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_order_product_urls_size"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="product_url",
        ),
    ]




