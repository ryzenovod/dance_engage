# Локальный запуск на macOS и деплой на Cloud.ru

Ниже — проверенный чек-лист для быстрого старта проекта на macOS и развертывания на виртуалке Cloud.ru (Ubuntu). Все команды выполняются в терминале.

## 1. Локальный запуск на macOS
1. **Установите зависимости ОС**: убедитесь, что стоят Python 3.9+, Git и Homebrew. При необходимости:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python@3.9 git
   ```
2. **Клонируйте репозиторий** и перейдите в папку проекта:
   ```bash
   git clone <repo-url> dance_engage
   cd dance_engage
   ```
3. **Создайте виртуальное окружение** и активируйте его:
   ```bash
   python3.9 -m venv .venv
   source .venv/bin/activate
   ```
4. **Установите зависимости**:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. **Создайте файл переменных окружения** `.env` в корне проекта:
   ```bash
   cat <<'ENV' > .env
   DJANGO_SECRET_KEY=change-me
   DEBUG=1
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ENV
   ```
6. **Примените миграции и создайте суперпользователя**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
7. **(Опционально) загрузите список танцев**:
   ```bash
   python manage.py load_dances
   ```
8. **Запустите сервер разработки**:
   ```bash
   python manage.py runserver
   ```
9. Откройте `http://127.0.0.1:8000` в браузере, войдите под суперпользователем.

## 2. Подготовка сервера Cloud.ru (Ubuntu)
1. **Создайте ВМ** в Cloud.ru (Ubuntu 22.04 LTS). Откройте порты 22 (SSH) и 80/443 (HTTP/HTTPS).
2. **Подключитесь по SSH**:
   ```bash
   ssh ubuntu@<public-ip>
   ```
3. **Обновите систему и установите пакеты**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3.10 python3.10-venv git nginx certbot python3-certbot-nginx
   ```
4. **Создайте системного пользователя для приложения** (по желанию):
   ```bash
   sudo adduser --system --group --home /opt/dance_engage danceapp
   sudo su - danceapp
   ```
5. **Клонируйте проект** и создайте виртуальное окружение:
   ```bash
   git clone <repo-url> /opt/dance_engage
   cd /opt/dance_engage
   python3.10 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. **Сконфигурируйте переменные окружения** в `/opt/dance_engage/.env` (обновите значения под прод):
   ```bash
   cat <<'ENV' > /opt/dance_engage/.env
   DJANGO_SECRET_KEY=<случайная_строка>
   DEBUG=0
   ALLOWED_HOSTS=<домен_или_IP>
   DATABASE_URL=sqlite:////opt/dance_engage/db.sqlite3
   ENV
   ```
   > При необходимости замените `DATABASE_URL` на подключение к PostgreSQL (например, `postgres://user:pass@localhost:5432/dance_engage`).
7. **Выполните миграции и загрузите данные**:
   ```bash
   source /opt/dance_engage/.venv/bin/activate
   cd /opt/dance_engage
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py load_dances
   ```
8. **Создайте сервис Gunicorn** `/etc/systemd/system/dance_engage.service`:
   ```bash
   sudo tee /etc/systemd/system/dance_engage.service > /dev/null <<'SERVICE'
   [Unit]
   Description=Dance Engage Gunicorn Service
   After=network.target

   [Service]
   User=danceapp
   Group=danceapp
   WorkingDirectory=/opt/dance_engage
   EnvironmentFile=/opt/dance_engage/.env
   ExecStart=/opt/dance_engage/.venv/bin/gunicorn dance_project.wsgi:application \\
       --bind 0.0.0.0:8000 \\
       --workers 3
   Restart=always

   [Install]
   WantedBy=multi-user.target
   SERVICE
   sudo systemctl daemon-reload
   sudo systemctl enable --now dance_engage
   sudo systemctl status dance_engage
   ```
9. **Настройте Nginx как реверс-прокси** `/etc/nginx/sites-available/dance_engage`:
   ```bash
   sudo tee /etc/nginx/sites-available/dance_engage > /dev/null <<'NGINX'
   server {
       listen 80;
       server_name <домен_или_IP>;

       location /static/ {
           alias /opt/dance_engage/static/;
       }

       location / {
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_pass http://127.0.0.1:8000;
       }
   }
   NGINX
   sudo ln -s /etc/nginx/sites-available/dance_engage /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```
10. **Включите HTTPS (если есть домен)**:
    ```bash
    sudo certbot --nginx -d <домен>
    sudo systemctl reload nginx
    ```
11. **Проверка**: откройте `http(s)://<домен_или_IP>` в браузере, убедитесь, что сайт отвечает.

## 3. Обновление кода на сервере
1. ```bash
   sudo su - danceapp
   cd /opt/dance_engage
   git pull
   source .venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   sudo systemctl restart dance_engage
   ```
2. Проверьте `sudo systemctl status dance_engage` и логи `journalctl -u dance_engage -f` при необходимости.

## 4. Полезные заметки
- Переменные окружения из `.env` подхватываются через `EnvironmentFile` в unit-файле systemd.
- Для PostgreSQL создайте пользователя/базу заранее: `sudo -u postgres createuser -P danceapp` и `createdb -O danceapp dance_engage`.
- Бэкапы SQLite делайте копированием файла `db.sqlite3`; для PostgreSQL используйте `pg_dump`.
- Если меняете домен/сертификаты, перезапустите Nginx: `sudo systemctl reload nginx`.
