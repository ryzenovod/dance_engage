# engage/management/commands/load_dances.py
from django.core.management.base import BaseCommand
from engage.models import Dance


class Command(BaseCommand):
    help = 'Load initial dance data into database'

    def handle(self, *args, **kwargs):
        dances = [
            # Вступительный танец
            {'name': 'Полонез', 'level': 'Начальный', 'has_partner': False},

            # I отделение
            {'name': 'Большой фигурный вальс', 'level': 'Средний', 'has_partner': False},
            {'name': 'Кадриль «Летучая мышь»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Богемская полька', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Вальс «Огонек Свечи»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Полька «Серпантин»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Марш «Возрождение»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Вальс «Под Амурские волны»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Дженни в базарный день»', 'level': 'Начальный', 'has_partner': False},

            # II отделение
            {'name': 'Вальс «Нежность»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Канон-галопад Кадриль', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Прихоть лорда Байрона»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Вальс «Графа Толстого»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Веселый парень»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'КД герцога Кентского', 'level': 'Начальный', 'has_partner': False},
            {'name': 'КД «Русский марш»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Корабельный повар»', 'level': 'Начальный', 'has_partner': False},

            # III отделение
            {'name': 'Шотландский вальс', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Юнион»', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Вальс «Паганини»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Тампет»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Вальс «Деревянная утка»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Полька Романи', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'КД «Пэмберли»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Вальс «Катрин»', 'level': 'Средний', 'has_partner': False},

            # IV отделение
            {'name': 'Вальс «Калейдоскоп»', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Вальс «Сердце зимы»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Морячка»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Вальс «Анастасия»', 'level': 'Средний', 'has_partner': False},
            {'name': 'Вальс «Ветер с гор»', 'level': 'Средний', 'has_partner': False},
            {'name': 'КД «Роувелл»', 'level': 'Начальный', 'has_partner': False},
            {'name': 'Блюз', 'level': 'Средний', 'has_partner': False},
            {'name': 'Вальс «Надежда»', 'level': 'Продвинутый', 'has_partner': False},
            {'name': 'Порушка', 'level': 'Начальный', 'has_partner': False}
        ]

        for dance in dances:
            Dance.objects.get_or_create(**dance)
            self.stdout.write(self.style.SUCCESS(f'Добавлен танец: {dance["name"]}'))

        self.stdout.write(self.style.SUCCESS('Все танцы успешно загружены!'))

