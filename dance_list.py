import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dance_project.settings')
django.setup()

from engage.dance_loader import sync_winter_ball_dances

if __name__ == "__main__":
    created = sync_winter_ball_dances()
    print(f"Танцы синхронизированы, новых записей: {created}")
