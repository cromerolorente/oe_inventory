"""Backfill delegation coordinates (latitude/longitude) from their address.

Usage:
    python manage.py geocode_delegations          # only delegations without coords
    python manage.py geocode_delegations --all     # re-geocode every delegation

Uses OpenStreetMap Nominatim and sleeps ~1s between requests to respect its
usage policy.
"""

import time

from django.core.management.base import BaseCommand

from oe_inventory_py_web.models import OeesDelegations
from oe_inventory_py_web.views import _geocode_delegation


class Command(BaseCommand):
    help = "Geocode delegations missing coordinates via OpenStreetMap Nominatim."

    def add_arguments(self, parser):
        parser.add_argument(
            '--all', action='store_true',
            help='Re-geocode every delegation, not only those missing coordinates.',
        )

    def handle(self, *args, **options):
        qs = OeesDelegations.objects.all().order_by('id_delegation')
        if not options['all']:
            qs = qs.filter(latitude__isnull=True)

        total = qs.count()
        self.stdout.write(f"Geocoding {total} delegation(s)...")
        done = 0
        for d in qs:
            prov = d.provincia.province if d.provincia else ''
            lat, lng = _geocode_delegation(d.direccion or '', d.cpostal or '', d.poblacion or '', prov)
            if lat is not None:
                d.latitude, d.longitude = lat, lng
                d.save(update_fields=['latitude', 'longitude'])
                done += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  [{d.id_delegation}] {d.delegation} -> {lat:.5f}, {lng:.5f}"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"  [{d.id_delegation}] {d.delegation} -> address not found"))
            time.sleep(1.1)  # Nominatim policy: max ~1 request/second

        self.stdout.write(self.style.SUCCESS(f"Done. Geocoded {done}/{total}."))
