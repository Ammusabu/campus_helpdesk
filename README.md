# Campus Helpdesk API

A backend helpdesk system built using **Django** and **Django Rest Framework** where students can raise complaints (tickets) and admins can manage and resolve them.

---

## Tech Stack

* Python
* Django
* Django Rest Framework
* PostgreSQL
* Redis
* JWT Authentication

---

## Features

* User registration & login
* JWT token authentication
* Create and view tickets
* Update ticket status
* Admin dashboard for managing users and tickets

---

## Setup

### 1. Clone the project

git clone https://github.com/<your-username>/campus_helpdesk.git
cd campus_helpdesk

### 2. Create virtual environment

python3 -m venv env
source env/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run migrations

python manage.py makemigrations
python manage.py migrate

### 5. Create admin user

python manage.py createsuperuser

### 6. Start server

python manage.py runserver

Open: http://127.0.0.1:8000/admin/

---

## API Authentication

Login returns a JWT token.

Add token in header:
Authorization: Bearer <token>

---

## Author

Ammu
