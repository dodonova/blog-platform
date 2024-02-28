# Blogicum

**For documentation in English, please refer to [README_EN.md](./README_EN.md).**

Проект Blogicum - это простая платформа для блогов. В проекте реализованы возможности: 
регистрация, создание, редактирование или удаление постов, отложенная публикация, комментирования постов другого автора.


### Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:dodonova/blog-platform.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Создать администратора и задать для него логин и пароль:
```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```
Локально  проект будем доступен по адресу: http://127.0.0.1:8000/

### Технологии

Python, Django Framework, SQLite.