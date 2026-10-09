# Blogicum — блог-платформа на Django

Сайт для публикаций: пользователи ведут свои блоги, публикуют посты с картинками и комментируют чужие записи.

## Возможности

- Регистрация, вход и смена пароля; страница профиля со всеми постами автора и редактирование профиля.
- Посты: создание, редактирование и удаление автором, загрузка изображений, отложенная публикация (пост с датой в будущем видит только автор).
- Категории и локации; снятые с публикации посты и категории скрыты от читателей.
- Комментарии: добавление, редактирование и удаление своих.
- Пагинация и счётчик комментариев у каждого поста.
- Собственные страницы ошибок 403, 404 и 500.
- Классовые представления (CBV) и миксины для проверки прав доступа.

## Технологии

Python 3.10+, Django 5.1, SQLite, Bootstrap 5, Pillow, Django Debug Toolbar, pytest.

## Как запустить

```bash
git clone https://github.com/Vantied/django-sprint4.git
cd django-sprint4
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd blogicum
python manage.py migrate
python manage.py loaddata db.json
python manage.py runserver
```

## Что я вынес из проекта

- Полный цикл разработки на Django: модели, ORM-запросы с аннотациями, формы, CBV, шаблоны.
- Разграничение прав доступа на уровне представлений.

## Автор

Иван Богатов — [GitHub](https://github.com/Vantied) · Telegram [@Ivan_bogatov55](https://t.me/Ivan_bogatov55)
