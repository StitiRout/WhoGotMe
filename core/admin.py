from django.contrib import admin

from .models import AttackInfo, Breach, BreachSourceStat, EmailCheck, MonthlyBreachStat


@admin.register(Breach)
class BreachAdmin(admin.ModelAdmin):
    list_display = ("email", "breach_name", "breach_date", "severity")
    list_filter = ("severity", "breach_name")
    search_fields = ("email", "breach_name")


admin.site.register(EmailCheck)
admin.site.register(AttackInfo)
admin.site.register(MonthlyBreachStat)
admin.site.register(BreachSourceStat)
