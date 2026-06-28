from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/check-email/", views.api_check_email, name="api_check_email"),
    path("api/attack-info/", views.api_attack_info, name="api_attack_info"),
]
