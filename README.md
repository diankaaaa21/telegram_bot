# Django Telegram Bot Project

Этот проект отправляет уведомления всем подписчикам Telegram-бота, когда любой пользователь успешно входит в админку Django.

## Стек

* Python
* Django
* pyTelegramBotAPI
* PostgreSQL
* Docker
* unittest (для тестов)

## Как запустить проект

1. Клонируй репозиторий:

```bash
git clone https://github.com/diankaaaa21/telegram_bot.git
cd telegram_bot
```

2. Собери и запусти контейнеры:

```bash
docker-compose up --build
```

3. Примените миграции:

```bash
docker-compose run web python manage.py migrate
```

4. Зайди на [http://localhost:8000/admin](http://localhost:8000/admin) и войди — бот отправит уведомление подписчикам.

---

## Как запустить тесты

Локально (без Docker):

```bash
python manage.py test app
```
В будущем для масштабируемости можно перейти на pytest с фикстурами.

---

## Команды бота

* `/start` или `/subscribe` — подписаться на уведомления.


