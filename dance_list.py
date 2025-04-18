# dance_list.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dance_project.settings')
django.setup()

from engage.models import Dance

dance_names = [
    "Венский вальс", "Медленный вальс", "Квикстеп", "Фокстрот", "Танго",
    "Ча-ча-ча", "Самба", "Румба", "Джайв", "Пасодобль",
    "Сальса", "Бачата", "Хастл", "Меренге", "Свинг",
    "Линди хоп", "Вест коуст свинг", "Контемп", "Дискофокс", "Полонез",
    "Мазурка", "Полька", "Кадриль", "Сиртаки", "Канкан",
    "Гопак", "Тарантелла", "Фламенко", "Аргентинское танго", "Балет"
]

for name in dance_names:
    Dance.objects.get_or_create(name=name)

print("Танцы успешно добавлены!")
