трое суток вайбкодинга, 2929 (иронично) строчек кода предназначенных
ЗАБАВЫ РАДИ, АХТУНГ, НЕ ВОСПРИНИМАЙТЕ ЭТО ВСЕРЬËЗ, просто из этого может получиться что-то интересное в дальнейшем, а пока просто побаловаться

прошу обратить внимание что проект стоит на моем ноуте (бюджет на аренду сервера ушел на покупку шаурмы), 
поэтому я не знаю, что будет, если туда зайдут 200 человек одновременно, если упадёт - подниму по возможности как смогу
об ошибках и багах просьба всемилостивейше сообщать в ЛС

инструкция по применению - обязательно перед выбором танцев в настройках выбрать роль - дама/кавалер/не определился (нужное подчеркнуть)
аватарки тоже не работают, и это не потому что мне лень и я хочу спать, а анонимности ради и сохранения антуража бала :)

прошу любить и жаловать https://dance-engage.serveo.net

---


## Как запустить локально на macOS

1. Поставьте свежий Python (например, 3.12) и Xcode Command Line Tools, чтобы корректно собиралась Pillow для аватарок: `xcode-select --install` и при необходимости `brew install python@3.12`.
2. Склонируйте проект и перейдите в папку: `git clone <repo-url> && cd dance_engage`.
3. Создайте и активируйте виртуальное окружение: `python3 -m venv .venv && source .venv/bin/activate`.
4. Обновите `pip` и установите зависимости: `python -m pip install --upgrade pip && pip install -r requirements.txt`.
5. Примените миграции и создайте суперпользователя при желании: `python manage.py migrate` и `python manage.py createsuperuser`.
6. Запустите дев-сервер: `python manage.py runserver 0.0.0.0:8000` и откройте http://localhost:8000/.
7. Если нужна чистая база или тестовые данные, удалите `db.sqlite3` и повторите шаг 5.

## Безопасность и устранение CSRF
- Перед продакшеном задайте собственный `DJANGO_SECRET_KEY` и выключите отладку переменной `DJANGO_DEBUG=false`.
- Для HTTPS включите `DJANGO_SECURE_SSL=true`, чтобы активировать защищённые куки, HSTS и редирект на https.
- Разрешённые хосты и доверенные источники CSRF настраиваются через `DJANGO_ALLOWED_HOSTS` и `DJANGO_CSRF_TRUSTED_ORIGINS` (списки через запятую). По умолчанию работают `localhost` и `127.0.0.1`.
- Все изменения состояния выполняются POST-запросами с `{% csrf_token %}`. Если видите 403 CSRF, убедитесь, что открываете сайт по доверенному домену/тумнелю и не блокируете куки.

## Как захостить на Cloud.ru (в ритме, но по делу)

1. **Подготовка проекта**
   - Убедитесь, что у вас есть Docker (для локальной проверки) и что в корне лежат `manage.py` и `requirements.txt`.
   - Выполните локально: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
   - Прогоните миграции: `python manage.py migrate` и создайте суперпользователя `python manage.py createsuperuser` при необходимости.

2. **Сборка образа**
   - Создайте `Dockerfile`, если его нет, с базовым образом `python:3.12-slim`, установкой зависимостей и командой запуска `gunicorn dance_project.wsgi:application --bind 0.0.0.0:8000`.
   - Соберите образ: `docker build -t dance-engage:latest .`.

3. **Загрузка в Container Registry Cloud.ru**
   - Залогиньтесь в CR: `cr login` (или через web-консоль получите данные для `docker login`).
   - Тегируйте образ: `docker tag dance-engage:latest cr.yandex/<project-id>/dance-engage:latest`.
   - Запушьте: `docker push cr.yandex/<project-id>/dance-engage:latest`.

4. **Развёртывание в Managed Kubernetes или Cloud.ru VM**
   - Для Kubernetes: создайте Deployment и Service, пробросьте порт 8000, подключите PersistentVolume для `media/` и переменные окружения (`DJANGO_SECRET_KEY`, `DEBUG=false`).
   - Для VM: поднимите VM с Ubuntu, поставьте Docker, запулите образ и запустите контейнер `docker run -d -p 80:8000 --env-file .env dance-engage:latest`.

5. **База данных и статика**
   - Лучше использовать управляемую PostgreSQL от Cloud.ru. Пропишите `DATABASE_URL` в `.env` и обновите `settings.py` на использование этого URL (через `dj-database-url`).
   - Соберите статические файлы: `python manage.py collectstatic --noinput` и храните их либо в S3-совместимом облаке Cloud.ru, либо внутри контейнера с reverse-proxy Nginx.

6. **Домен и HTTPS**
   - Подключите домен через DNS Cloud.ru и выпустите сертификат (например, c certbot на VM или через ingress-контроллер в Kubernetes).

7. **Мониторинг**
   - Включите логи контейнера в Log Storage, настройте алерты по перезагрузкам и латентности HTTP, чтобы знать, если бал внезапно упадёт.
