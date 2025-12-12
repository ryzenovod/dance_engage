from django.db import migrations
from engage.dance_data import WINTER_BALL_DANCES


def seed_winter_ball_dances(apps, schema_editor):
    Dance = apps.get_model('engage', 'Dance')
    for dance in WINTER_BALL_DANCES:
        Dance.objects.update_or_create(
            name=dance["name"],
            defaults={
                "level": dance["level"],
                "has_partner": dance.get("has_partner", False),
            },
        )


def remove_winter_ball_dances(apps, schema_editor):
    Dance = apps.get_model('engage', 'Dance')
    names = [dance["name"] for dance in WINTER_BALL_DANCES]
    Dance.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('engage', '0002_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.RunPython(seed_winter_ball_dances, remove_winter_ball_dances),
    ]
