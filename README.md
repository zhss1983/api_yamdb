# Документация к API YaMDb (v1)

## Описание проекта:

Проект YaMDb собирает отзывы пользователей на различные произведения
сохранённые в базе данных (БД) проекта. Произведения делятся на категории:
«Книги», «Фильмы», «Музыка» и т.д. Список категорий может быть расширен
администратором (например, можно добавить категорию «Изобразительное искусство»
или «Ювелирка»).

Система не хранит в своей БД YaMDb исходный контент, нельзя посмотреть фильм
или послушать музыку.

Новые произведения могут вносить только администраторы, для рядовых
пользователей данный функционал недоступен. Произведению может быть присвоен
жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Новые жанры также может создавать только администратор.

Предложенное API можно использовать как самостоятельный проект, а можно 
доработать под конкретные требования.

### Технологии

Python 3.8, Postgres 12.4, Nginx 1.21.4, Gunicorn 20, Django 3, Django REST Framework (Filters, Pagination, Permissions, Mixins, Viewsets).

## Как запустить проект:

Если вы собираетесь работать из командной строки в **windows**, вам может
 потребоваться Bash. Скачать его можно по ссылке:
 [GitBash](https://gitforwindows.org/) ([Git-2.33.0.2-64-bit.exe](https://github.com/git-for-windows/git/releases/download/v2.33.0.windows.2/Git-2.33.0.2-64-bit.exe)).

Так же при работе в **windows** необходимо использовать **python** вместо
 **python3**

Последнюю версию **python** ищите на официальном сайте
 [https://www.python.org/](https://www.python.org/downloads/)

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/zhss1983/api_yamdb
```

```
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```
python -m venv env
```

- linux
>```
>source env/bin/activate
>```
- windows
>```
>source env/Scripts/activate
>```

Установить зависимости из файла **requirements.txt**:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в подкаталог yatube_api и выполнить миграции:

```
cd api_yamdb
python manage.py migrate
```

Создать администратора (суперпользователя) БД:

```
python manage.py createsuperuser
```

Запустить проект:

```
python manage.py runserver
```

## Работа с эндпоинтами:

Краткое описание основных возможностей, за более подробной информацией
обратитесь к [/redoc/](http://127.0.0.1:8000/redoc/) 

### Авторизация с применением JWT токена

#### Регистрация нового пользователя

Для получения JWT-токена необходимо отправить **JSON** запрос, содержащий
имя пользователя и имя почтового ящика.

**JSON** запрос:

```JSON
{
  "email": "string",
  "username": "string"
}
```

POST: [/api/v1/auth/signup/](http://127.0.0.1:8000/api/v1/auth/signup/)

В письме придёт код подтверждения. Дальше необходимо необходимо отправить
**JSON** запрос, содержащий код подтверждения:

```JSON
{
  "username": "string",
  "confirmation_code": "string"
}
```

POST: [/api/v1/auth/token/](http://127.0.0.1:8000/api/v1/auth/token/)

В ответ вы получите токен для доступа к сервису.

```JSON
{
  "token": "string"
}
```

Вам будут доступны:
- Категории:
  [/api/v1/categories/](http://127.0.0.1:8000/api/v1/categories/)
- Жанры:
  [/api/v1/genres/](http://127.0.0.1:8000/api/v1/genres/)
- Произведения:
  [/api/v1/titles/](http://127.0.0.1:8000/api/v1/titles/)
- Отзывы:
  [/api/v1/titles/{title_id}/reviews/](http://127.0.0.1:8000/api/v1/titles/1/reviews/)
- Комментарии:
  [/api/v1/titles/{title_id}/reviews/{review_id}/comments/](http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/)
 
По всем вопросам обращайтесь к администраторам по электронной почте
[ask@api_yamdb.ru](mailto:ask@api_yamdb.ru)
