import json

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .models import AttackInfo, BreachSourceStat, EmailCheck, MonthlyBreachStat
from .services import check_email, validate_email


def landing(request):
    return render(request, "core/landing.html")


def dashboard(request):
    timeline = list(
        MonthlyBreachStat.objects.values("month", "breach_count").order_by("sort_order")
    )
    sources = list(
        BreachSourceStat.objects.values("source", "count").order_by("sort_order")
    )

    total_checks = EmailCheck.objects.count()
    breached_checks = EmailCheck.objects.filter(is_clean=False).count()
    critical_checks = EmailCheck.objects.filter(risk_score__gte=75).count()

    risk_dist = [
        {"name": "Critical", "value": 18, "color": "#ff3864"},
        {"name": "High", "value": 31, "color": "#f59e0b"},
        {"name": "Medium", "value": 34, "color": "#00f0ff"},
        {"name": "Low", "value": 17, "color": "#00ff88"},
    ]

    context = {
        "chart_data": {
            "timeline": timeline,
            "sources": sources,
            "riskDist": risk_dist,
            "apiAttack": reverse("api_attack_info"),
        },
        "stats": {
            "total_breaches": "8,947",
            "emails_at_risk": "1.24B",
            "critical_users": f"{critical_checks:,}" if critical_checks else "218K",
            "new_breaches": "61",
            "total_checks": total_checks,
            "breached_checks": breached_checks,
        },
    }
    return render(request, "core/dashboard.html", context)


@require_POST
def api_check_email(request):
    try:
        payload = json.loads(request.body)
        email = payload.get("email", "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    if not validate_email(email):
        return JsonResponse({"error": "Invalid email address."}, status=400)

    ip = request.META.get("REMOTE_ADDR")
    result = check_email(email, ip_address=ip)
    return JsonResponse(result)


@require_GET
def api_attack_info(request):
    query = request.GET.get("q", "").strip().lower()
    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required."}, status=400)

    attack = AttackInfo.objects.filter(slug=query).first()
    if not attack:
        attack = AttackInfo.objects.filter(name__iexact=query).first()

    if not attack:
        return JsonResponse(
            {
                "found": False,
                "query": query,
                "suggestions": ["SQL Injection", "Phishing", "Ransomware", "XSS", "DDoS"],
            }
        )

    return JsonResponse(
        {
            "found": True,
            "query": attack.name,
            "data": {
                "summary": attack.summary,
                "vector": attack.vector,
                "mitigation": attack.mitigation,
                "cve": attack.cve,
            },
        }
    )
