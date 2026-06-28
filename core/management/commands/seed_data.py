from django.core.management.base import BaseCommand

from core.models import AttackInfo, BreachSourceStat, MonthlyBreachStat


class Command(BaseCommand):
    help = "Seed dashboard charts and attack intelligence data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding dashboard data...")

        timeline = [
            ("Jan", 12), ("Feb", 19), ("Mar", 8), ("Apr", 27),
            ("May", 34), ("Jun", 21), ("Jul", 45), ("Aug", 38),
            ("Sep", 52), ("Oct", 29), ("Nov", 61), ("Dec", 44),
        ]
        for i, (month, count) in enumerate(timeline):
            MonthlyBreachStat.objects.update_or_create(
                month=month,
                defaults={"year": 2024, "breach_count": count, "sort_order": i},
            )

        sources = [
            ("Social Media", 142),
            ("E-Commerce", 98),
            ("Healthcare", 75),
            ("Finance", 61),
            ("Gaming", 48),
            ("Education", 33),
        ]
        for i, (source, count) in enumerate(sources):
            BreachSourceStat.objects.update_or_create(
                source=source,
                defaults={"count": count, "sort_order": i},
            )

        attacks = [
            {
                "slug": "sql injection",
                "name": "SQL Injection",
                "summary": "Attacker inserts malicious SQL into input fields to manipulate database queries.",
                "vector": "Network – untrusted user input passed directly to SQL interpreter.",
                "mitigation": "Parameterized queries, prepared statements, input validation, WAF.",
                "cve": "CWE-89",
            },
            {
                "slug": "phishing",
                "name": "Phishing",
                "summary": "Social engineering attack using deceptive emails or sites to steal credentials.",
                "vector": "Human – convincing impersonation of trusted entities via email or web.",
                "mitigation": "MFA, DMARC/DKIM/SPF, security awareness training, URL filtering.",
                "cve": "",
            },
            {
                "slug": "ransomware",
                "name": "Ransomware",
                "summary": "Malware that encrypts victim files and demands payment for decryption keys.",
                "vector": "Phishing, RDP exploitation, drive-by downloads.",
                "mitigation": "Offline backups, EDR, network segmentation, patch management.",
                "cve": "CVE-2021-34527",
            },
            {
                "slug": "xss",
                "name": "XSS",
                "summary": "Cross-Site Scripting injects malicious scripts into pages viewed by other users.",
                "vector": "Browser – reflected, stored, or DOM-based injection.",
                "mitigation": "Content Security Policy, output encoding, HttpOnly cookies.",
                "cve": "CWE-79",
            },
            {
                "slug": "ddos",
                "name": "DDoS",
                "summary": "Distributed Denial of Service overwhelms target systems with massive traffic.",
                "vector": "Network – botnets flood bandwidth or exhaust server resources.",
                "mitigation": "CDN rate-limiting, anycast routing, traffic scrubbing, upstream filtering.",
                "cve": "",
            },
            {
                "slug": "man in the middle",
                "name": "Man in the Middle",
                "summary": "Attacker secretly intercepts and relays communication between two parties.",
                "vector": "Network – ARP spoofing, rogue WiFi, SSL stripping.",
                "mitigation": "TLS/HTTPS everywhere, certificate pinning, HSTS, DNSSEC.",
                "cve": "",
            },
        ]
        for data in attacks:
            AttackInfo.objects.update_or_create(slug=data["slug"], defaults=data)

        self.stdout.write(self.style.SUCCESS("Dashboard data seeded successfully."))
