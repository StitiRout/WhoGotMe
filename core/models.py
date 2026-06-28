from django.db import models


class Breach(models.Model):
    """Maps to the `breaches` table from thedb.sql."""

    breach_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, db_index=True)
    breach_name = models.CharField(max_length=100)
    breach_date = models.DateField()
    data_exposed = models.CharField(max_length=255)
    severity = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        db_table = "breaches"
        ordering = ["-breach_date"]

    def __str__(self):
        return f"{self.email} — {self.breach_name}"


class EmailCheck(models.Model):
    email = models.EmailField()
    is_clean = models.BooleanField()
    risk_score = models.PositiveSmallIntegerField(default=0)
    breach_count = models.PositiveSmallIntegerField(default=0)
    checked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-checked_at"]

    def __str__(self):
        status = "clean" if self.is_clean else "breached"
        return f"{self.email} ({status})"


class AttackInfo(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    summary = models.TextField()
    vector = models.TextField()
    mitigation = models.TextField()
    cve = models.CharField(max_length=32, blank=True)

    class Meta:
        verbose_name_plural = "attack info"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MonthlyBreachStat(models.Model):
    month = models.CharField(max_length=8, unique=True, help_text="Short month label, e.g. Jan")
    year = models.PositiveSmallIntegerField(default=2024)
    breach_count = models.PositiveIntegerField()
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.month} {self.year}: {self.breach_count}"


class BreachSourceStat(models.Model):
    source = models.CharField(max_length=80, unique=True)
    count = models.PositiveIntegerField()
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.source}: {self.count}"
