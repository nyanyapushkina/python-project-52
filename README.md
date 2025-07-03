# Task Manager

[![Actions Status](https://github.com/nyanyapushkina/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/nyanyapushkina/python-project-52/actions) [![Maintainability](https://qlty.sh/badges/ce7e4819-ad08-48cf-aa1f-3524b9fd45fa/maintainability.svg)](https://qlty.sh/gh/nyanyapushkina/projects/python-project-52) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nyanyapushkina_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nyanyapushkina_python-project-52)

Task Manager is a simple but powerful system for managing tasks. Create tasks, assign performers and update statuses – all in one place.

## Demo

Live demo available at: [https://python-project-52-3ho6.onrender.com](https://python-project-52-3ho6.onrender.com)

## Features

- Create and manage tasks
- Assign tasks to team members
- Track task statuses
- User authentication system
- Responsive design

## Installation

### Prerequisites
- Python 3.9+

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/nyanyapushkina/python-project-52.git
   cd python-project-52
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   # OR
   venv\Scripts\activate    # Windows
3. Install dependencies:
   ```bash
   pip install -e .
4. Configure environment:
Create .env file in the project root:
	```ini
	SECRET_KEY=your_django_secret_key
    DATABASE_URL=postgres://
5. Database setup:
	```bash
	python manage.py migrate
6. Create admin user:
	```bash
	python manage.py createsuperuser
7. Run the server:
    ```bash
	python manage.py runserver
## Contact

For any inquiries, please contact me at:  
📧  [khokhlova.arina.v@gmail.com](https://mailto:khokhlova.arina.v@gmail.com/)