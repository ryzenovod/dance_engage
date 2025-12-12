from django.db import transaction

from .models import Dance
from .dance_data import WINTER_BALL_DANCES, LEVEL_ORDER


def sync_winter_ball_dances():
    created = 0
    with transaction.atomic():
        for dance in WINTER_BALL_DANCES:
            _, is_created = Dance.objects.update_or_create(
                name=dance["name"],
                defaults={
                    "level": dance["level"],
                    "has_partner": dance.get("has_partner", False),
                },
            )
            created += int(is_created)
    return created


def ensure_dances_seeded():
    if not Dance.objects.exists():
        sync_winter_ball_dances()
    return Dance.objects.all()
