# Student_Management_System
 

A Django-based School Management System with AI analytics and automated workflows for educational institutions.

## Features

- **Student Management**: Complete student profiles with parent information
- **Teacher Management**: Teacher profiles and subject assignments  
- **Bulk Import**: CSV-based student import (95% time savings)
- **AI Analytics**: Machine learning for performance prediction
- **Notifications**: Real-time alerts for all activities
- **Role-Based Access**: Different dashboards for students, teachers, and admins

## Technology Stack

- **Framework**: Django 5.2.5
- **Language**: Python 3.13.1
- **Database**: SQLite3 / PostgreSQL
- **ML**: scikit-learn for predictive analytics
- **Testing**: 28 automated tests with 90% coverage
- **CI/CD**: GitHub Actions automation

## Quick Start

1. Clone repository:
```bash
git clone https://github.com/KAVINADINIVEDYA/Student_Management_System.git
cd Student_Management_System
```

2. Setup environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Database setup:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. Run server:
```bash
python manage.py runserver
```

5. Access at `http://127.0.0.1:8000/`

## Key Highlights

- **Bulk Processing**: Import hundreds of students instantly via CSV
- **Predictive Analytics**: AI identifies at-risk students automatically
- **Automated Testing**: 28 tests ensure system reliability
- **Clean Architecture**: Modular design with separation of concerns
- **Production Ready**: CI/CD pipeline with quality gates

## Testing

Run all tests:
```bash
python manage.py test
```

Check coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

## Project Structure

```
Student_Management_System/
├── home_auth/          # Authentication system
├── student/            # Student management
├── teacher/            # Teacher management  
├── subject/            # Subject management
├── school/             # Notifications & dashboard
├── analytics/          # AI/ML analytics
└── templates/          # HTML templates
```

## Author

**KAVINA DINIDEDYA**
- GitHub: @KAVINADINIVEDYA

 
