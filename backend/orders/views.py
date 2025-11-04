import json
from typing import Any

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task

from .models import Order
from .services.buy_with_browser_use import buy_product


def _purchase_async(order_id: int, product_url: str) -> None:
    # retained for backward compatibility if needed; prefer Q task
    from .tasks import process_order
    process_order(order_id)


@csrf_exempt
def buy(request: HttpRequest) -> HttpResponse:
    if request.method == "OPTIONS":
        resp = HttpResponse()
        resp["Access-Control-Allow-Origin"] = "http://localhost:5173"
        resp["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        resp["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        payload: dict[str, Any] = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    # Accept either a single URL or a list of URLs (single will be converted)
    product_urls = payload.get("product_urls")
    product_url = payload.get("product_url")
    size = payload.get("size") or "Medium"

    urls: list[str] | None = None
    if isinstance(product_urls, list) and all(isinstance(u, str) for u in product_urls):
        urls = product_urls
    elif isinstance(product_url, str):
        urls = [product_url]

    if not urls:
        return JsonResponse({"detail": "product_urls (list[str]) or product_url (str) is required"}, status=400)

    # Create order record with multi-URL support only
    order = Order.objects.create(
        product_urls=urls,
        size=str(size),
        status=Order.Status.QUEUED,
    )

    # Enqueue task on Q Cluster so frontend isn't blocked
    async_task("orders.tasks.process_order", order.id)

    resp = JsonResponse({"status": "accepted", "order_id": order.id}, status=202)
    resp["Access-Control-Allow-Origin"] = "http://localhost:5173"
    return resp


