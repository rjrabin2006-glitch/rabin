# EduMind AI - Installation Guide

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **MySQL**: 5.7 or higher
- **RAM**: 4GB minimum
- **Disk Space**: 2GB minimum
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## Step 1: Install Prerequisites

### Windows

1. **Install Python**
   - Download from: https://www.python.org/downloads/
   - Run installer, check "Add Python to PATH"
   - Verify: `python --version`

2. **Install MySQL**
   - Download from: https://www.mysql.com/downloads/mysql/
   - Run installer, complete setup
   - Start MySQL Service
   - Verify: `mysql --version`

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Install MySQL
brew install mysql
mysql.server start
```

### Ubuntu/Linux

```bash
# Update system
sudo apt-get update

# Install Python
sudo apt-get install python3 python3-pip python3-venv

# Install MySQL
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

## Step 2: Clone Repository

```bash
git clone <repository-url>
cd EduMind-AI
```

## Step 3: Setup Python Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 4: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 5: Setup Database

### Create Database User

```bash
mysql -u root -p
```

Inside MySQL:

```sql
CREATE USER 'edumind_user'@'localhost' IDENTIFIED BY 'edumind_password';
GRANT ALL PRIVILEGES ON edumind_db.* TO 'edumind_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Import Database Schema

```bash
mysql -u edumind_user -p edumind_db < schema.sql
```

### Verify Database

```bash
mysql -u edumind_user -p edumind_db
SHOW TABLES;
SELECT COUNT(*) FROM students;
EXIT;
```

## Step 6: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your database credentials:
   ```
   DB_HOST=localhost
   DB_USER=edumind_user
   DB_PASSWORD=edumind_password
   DB_NAME=edumind_db
   ```

## Step 7: Train Machine Learning Model

```bash
python model.py
```

Expected output:
```
============================================================
EduMind AI - Student Performance Prediction Model
============================================================

No model found. Training new model...

--- Data Cleaning ---
✓ Data cleaning completed: 950 records remaining

--- Feature Selection ---
Features: ['internal_marks', 'assignment_marks', ...]
Target: risk_level (0=Low, 1=Medium, 2=High)
✓ Features selected: 6 features, 950 samples

--- Model Training ---

Training set: 760 samples
Testing set: 190 samples

Training Random Forest Classifier...
✓ Model training completed

--- Model Evaluation ---
Accuracy:  0.8763
Precision: 0.8821
Recall:    0.8763
F1-Score:  0.8780
```

## Step 8: Run Application

```bash
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

## Step 9: Access Application

1. Open browser: http://localhost:5000
2. Login with credentials:
   - **Admin**: admin@edumind.com / admin123
   - **Faculty**: faculty@edumind.com / faculty123

## VS Code Setup (Optional but Recommended)

### Install Extensions

1. **Python Extension Pack** by Don Jayamanne
2. **Pylance** by Microsoft
3. **Flask** by Dong Yoon Park
4. **MySQL** by Weijan Chen

### VS Code Settings

Create `.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.pythonPath": "${workspaceFolder}/venv/bin/python",
    "[python]": {
        "editor.formatOnSave": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### Launch Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_ENV": "development"
            },
            "args": ["run"],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

## Troubleshooting

### MySQL Connection Error

**Problem**: `Access denied for user 'root'@'localhost'`

**Solution**:
```bash
mysql -u root -p
FLUSH PRIVILEGES;
EXIT;
```

### Port Already in Use

**Problem**: `Address already in use`

**Solution**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Model Training Error

**Problem**: `FileNotFoundError: dataset/student_data.csv`

**Solution**:
1. Ensure dataset file exists
2. Check file path is correct
3. Run: `python model.py`

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL service running
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database created and populated
- [ ] ML model trained
- [ ] Application running on port 5000
- [ ] Can login successfully
- [ ] Dashboard displays student data

## Next Steps

After successful installation:

1. Review `QUICK_START.md` for basic usage
2. Check documentation in `/docs` folder
3. Run test suite: `pytest tests/`
4. Explore the admin dashboard

## Support

For issues:
1. Check troubleshooting section
2. Review application logs
3. Create issue in repository

---

**Installation Guide v1.0** | Last Updated: 2026-06-12
