from __future__ import annotations

import json
import os
from typing import Any

from .models import Order
from .services.buy_with_browser_use import buy_products, buy_product


def process_order(order_id: int) -> None:
    os.environ["USER_PASSWORD"] = "GreatPW!12"
    order = Order.objects.get(pk=order_id)
    if order.status not in {Order.Status.QUEUED, Order.Status.FAILED}:
        return

    order.status = Order.Status.RUNNING
    order.save(update_fields=["status", "updated_at"])

    try:
        # Use multi-URL list exclusively
        urls: list[str] = [str(u) for u in (order.product_urls or [])]
        if not urls:
            raise ValueError("Order has no product URLs")

        history = buy_products(urls, getattr(order, "size", "Medium"))
        try:
            logs_json: dict[str, Any] | list[Any] | None = json.loads(json.dumps(history, default=str))
        except Exception:
            logs_json = None

        order.status = Order.Status.SUCCESS
        order.logs = logs_json
        order.logs_text = str(history)
        order.error_message = ""
        order.save(update_fields=["status", "logs", "logs_text", "error_message", "updated_at"])
    except Exception as exc:  # noqa: BLE001
        order.status = Order.Status.FAILED
        order.error_message = str(exc)
        order.save(update_fields=["status", "error_message", "updated_at"])


