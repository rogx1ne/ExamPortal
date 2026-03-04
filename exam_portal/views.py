from __future__ import annotations

import os

from django.db import connections
from django.http import JsonResponse


def health_check(request):
    payload: dict[str, object] = {"status": "ok"}

    if os.environ.get("DJANGO_HEALTHCHECK_DB", "").strip() == "1":
        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            payload["db"] = "ok"
        except Exception:
            return JsonResponse({"status": "degraded", "db": "error"}, status=503)

    return JsonResponse(payload)
