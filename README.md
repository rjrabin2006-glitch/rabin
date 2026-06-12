# EduMind AI - Intelligent Student Learning & Performance Analytics System

## Project Overview

EduMind AI is a comprehensive web-based system for analyzing student academic performance and predicting learning outcomes using Machine Learning. The system provides faculty and administrators with actionable insights into student performance while offering personalized recommendations to improve learning outcomes.

## Features

- **Student Performance Analytics**: Comprehensive tracking of marks, attendance, and academic progress
- **AI-Powered Predictions**: ML-based prediction of student risk levels (Low, Medium, High)
- **Attendance Monitoring**: Real-time attendance tracking and alerts
- **Personalized Recommendations**: Automated recommendations based on student performance
- **Faculty Dashboard**: Analytics and insights for educators
- **Interactive Reports**: Detailed performance reports and analytics
- **Responsive UI**: Modern, mobile-friendly interface with Bootstrap 5
- **Real-time Analytics**: Chart.js integration for data visualization

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL
- **ORM**: Flask-SQLAlchemy

### Machine Learning
- **Model**: Random Forest Classifier
- **Libraries**: scikit-learn, pandas, numpy

### Frontend
- **HTML/CSS**: Bootstrap 5
- **JavaScript**: ES6+
- **Charts**: Chart.js

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### Steps

1. **Clone Repository**
```bash
git clone <repository-url>
cd EduMind-AI
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Database**
```bash
mysql -u root -p < schema.sql
```

5. **Configure Database**
Edit `config.py` with your database credentials

6. **Train ML Model**
```bash
python model.py
```

7. **Run Application**
```bash
python app.py
```

Application will be available at `http://localhost:5000`

## Project Structure

```
EduMind-AI/
├── app.py                    # Flask application
├── database.py               # Database configuration
├── model.py                  # ML model
├── requirements.txt          # Python dependencies
├── schema.sql                # Database schema
├── config.py                 # Configuration
├── dataset/
│   └── student_data.csv      # Training data
├── models/
│   └── trained_model.pkl     # Trained ML model
├── templates/
│   ├── base.html             # Base template
│   ├── login.html            # Login page
│   ├── dashboard.html        # Admin dashboard
│   ├── students.html         # Students list
│   ├── add_student.html      # Add student
│   ├── edit_student.html     # Edit student
│   ├── prediction.html       # Prediction page
│   ├── reports.html          # Reports page
│   └── faculty_dashboard.html # Faculty dashboard
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   └── js/
│       └── script.js         # JavaScript
└── docs/
    ├── ER_DIAGRAM.md         # ER Diagram
    ├── USE_CASES.md          # Use cases
    ├── DFD.md                # Data flow diagrams
    └── ARCHITECTURE.md       # System architecture
```

## Usage

### Login
- Default Admin: `admin@edumind.com` / `admin123`
- Default Faculty: `faculty@edumind.com` / `faculty123`

### Dashboard
- View overall student performance
- Monitor attendance rates
- Check risk predictions
- Access analytics

### Student Management
- Add/Edit/Delete students
- Track marks and attendance
- View individual predictions

### Reports
- Generate performance reports
- Export data
- View analytics

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /logout` - User logout

### Dashboard
- `GET /` - Home page
- `GET /dashboard` - Admin dashboard
- `GET /faculty_dashboard` - Faculty dashboard

### Students
- `GET /students` - List all students
- `POST /add_student` - Add new student
- `GET /edit_student/<id>` - Edit student
- `POST /update_student/<id>` - Update student
- `GET /delete_student/<id>` - Delete student

### Predictions & Analytics
- `GET /predict` - Prediction page
- `POST /api/predict` - Get prediction
- `GET /reports` - Reports page

## Machine Learning Model

### Model Type
- Algorithm: Random Forest Classifier
- Risk Levels:
  - **LOW**: CGPA >= 8.0
  - **MEDIUM**: CGPA >= 6.5 and < 8.0
  - **HIGH**: CGPA < 6.5

### Features
- Internal Marks
- Assignment Marks
- Practical Marks
- External Marks
- Attendance
- Number of Subjects

## Recommendations Engine

The system automatically generates personalized recommendations:

- **Attendance < 75%**: Show attendance warning
- **Internal Marks < 60**: Recommend revision classes
- **Assignment Marks < 60**: Recommend practice assignments

## Documentation

Detailed documentation available in `/docs` folder:
- ER Diagram
- Use Case Diagram
- Data Flow Diagrams (Level 0 & 1)
- System Architecture

## Testing

Run test suite:
```bash
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please follow:
1. Code style: PEP 8
2. Write tests for new features
3. Update documentation

## License

MIT License - See LICENSE file

## Authors

EduMind AI Development Team

## Support

For issues and support, please create an issue in the repository.

---

**Last Updated**: 2026-06-12
