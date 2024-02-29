# Blogicum

The Blogicum project is a simple blogging platform. The project implements the following features:
registration, creation, editing or deleting posts, delayed publication, commenting on posts of another author.


### Installation

Clone the repository and go to it on the command line:

```
git clone git@github.com:dodonova/blog-platform.git
```

```
cd blog-platform
```

Create and activate a virtual environment:

```
python3 -m venv env
```

* If you have Linux/macOS

     ```
     source env/bin/activate
     ```

* If you have windows

     ```
     source env/scripts/activate
     ```

```
python3 -m pip install --upgrade pip
```

Install dependencies from the requirements.txt file:

```
pip install -r requirements.txt
```

Run migrations:

```
python3 manage.py migrate
```

Create an administrator and set a login and password for him:
```
python3 manage.py createsuperuser
```

Run the project:

```
python3 manage.py runserver
```
Locally on your computer the project will be available at: http://127.0.0.1:8000/

### Technologies

Python, Django Framework, SQLite.

---