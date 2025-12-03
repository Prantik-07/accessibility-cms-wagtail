# Wagtail Accessibility CMS

Web-based accessibility audit tool built with Wagtail CMS and pa11y.

## Features

- Automated accessibility scanning with pa11y
- WCAG violation tracking
- Audit history and reporting
- Wagtail admin interface
- RESTful API support

## Prerequisites

- Python 3.8+
- Node.js (for pa11y)
- pa11y: 
pm install -g pa11y

## Installation

1. Clone the repository
2. Create virtual environment: python -m venv venv
3. Activate: env\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
4. Install dependencies: pip install -r requirements.txt
5. Run migrations: python manage.py migrate
6. Create superuser: python manage.py createsuperuser
7. Run server: python manage.py runserver

## Usage

1. Access admin at http://127.0.0.1:8000/admin/
2. Create an Audit Index Page from Pages
3. Use 'Run Audit' from admin menu to scan pages
4. View results in Audit Records

## Technologies

- Wagtail 7.2+
- Django 5.2+
- pa11y
- Tailwind CSS

## License

MIT License
