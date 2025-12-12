# engage/management/commands/load_dances.py
from django.core.management.base import BaseCommand
from engage.models import Dance


class Command(BaseCommand):
    help = 'Load initial dance data into database'

    def handle(self, *args, **kwargs):
        dances = [
            # Программа Зимнего бала ДВФУ 2025
            {'name': 'Полонез', 'level': 'Начальный', 'has_partner': False},

            # 1-е отделение
            {'name': 'Большой фигурный вальс', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Кадриль «Летучая мышь»', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Богемская полька', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Вальс «Огонек Свечи»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'КД «Три орешка для Золушки»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Канон-галапад Кадриль', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Вальс «Паганини»', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Катильон с цветком', 'level': 'Начальный', 'has_partner': False},

            # 2-е отделение
            {'name': 'Вальс «Нежность»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Полька «Диабло»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Зимний Сон»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Фри Массон', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Вальс «Сердце зимы»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Пожарники»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Вальс «Графа Толстого»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Ирландская полька', 'level': 'Начальный', 'has_partner': False},

            # 3-е отделение
            {'name': 'Вальс «Катрин»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Романи полька', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Вальс «Прогулка»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Шотланский Вальс', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Бретонская линейная джига', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Вальс «Анастасия»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Русский Марш»', 'level': 'Средний', 'has_partner': False},
            {'name': 'БФ Вальс', 'level': 'Продвинутый', 'has_partner': False},

            # 4-е отделение
            {'name': 'Вальс «Калейдоскоп»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Вальс «Ветер с гор»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Роувелл»', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Вальс «Надежда»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Блюз', 'level': 'Средний', 'has_partner': False},
            {'name': 'Вальс «Память»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Порушка', 'level': 'Начальный', 'has_partner': False}
        ]

        for dance in dances:
            Dance.objects.get_or_create(**dance)
            self.stdout.write(self.style.SUCCESS(f'Добавлен танец: {dance["name"]}'))

        self.stdout.write(self.style.SUCCESS('Все танцы успешно загружены!'))

