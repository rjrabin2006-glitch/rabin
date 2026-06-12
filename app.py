"""app.py
============================================================
Flask Application - EduMind AI Main Application
Purpose: Main Flask app with all routes and business logic
Author: EduMind AI Development Team
Created: 2026
============================================================"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import local modules
from database import (
    db, User, Student, Subject, Mark, Attendance, Prediction, Recommendation,
    DatabaseOperations
)
from model import PredictionModel
from config import config

# Load environment variables
load_dotenv()

# ============================================================
# FLASK APP INITIALIZATION
# ============================================================

def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        init_default_data()
    
    # Setup login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints and routes
    register_routes(app)
    
    # Error handlers
    register_error_handlers(app)
    
    return app


def init_default_data():
    """Initialize default users and subjects"""
    # Check if admin already exists
    if User.query.filter_by(email='admin@edumind.com').first():
        return
    
    # Create admin user
    admin_user, _ = DatabaseOperations.create_user(
        username='admin',
        email='admin@edumind.com',
        password='admin123',
        role='admin',
        first_name='Admin',
        last_name='User'
    )
    
    # Create faculty user
    faculty_user, _ = DatabaseOperations.create_user(
        username='faculty1',
        email='faculty@edumind.com',
        password='faculty123',
        role='faculty',
        first_name='Faculty',
        last_name='Member'
    )
    
    # Create default subjects
    subjects_data = [
        {'code': 'CS101', 'name': 'Data Structures', 'credits': 4, 'semester': 1},
        {'code': 'CS102', 'name': 'Web Development', 'credits': 3, 'semester': 1},
        {'code': 'CS103', 'name': 'Database Management', 'credits': 3, 'semester': 2},
        {'code': 'CS104', 'name': 'Machine Learning', 'credits': 4, 'semester': 3},
        {'code': 'CS105', 'name': 'Cloud Computing', 'credits': 3, 'semester': 3},
    ]
    
    for subject_data in subjects_data:
        DatabaseOperations.create_subject(**subject_data)


def register_routes(app):
    """Register all application routes"""
    
    # ==================== AUTHENTICATION ROUTES ====================
    
    @app.route('/', methods=['GET'])
    def index():
        """Home page/Dashboard redirect"""
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('dashboard'))
            elif current_user.role == 'faculty':
                return redirect(url_for('faculty_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        return redirect(url_for('login'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login"""
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            
            # Validate input
            if not email or not password:
                flash('Email and password are required.', 'error')
                return render_template('login.html')
            
            # Authenticate user
            user = DatabaseOperations.authenticate_user(email, password)
            if user and user.is_active:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid email or password.', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout', methods=['GET'])
    @login_required
    def logout():
        """User logout"""
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('login'))
    
    # ==================== ADMIN DASHBOARD ====================
    
    @app.route('/dashboard', methods=['GET'])
    @login_required
    def dashboard():
        """Admin dashboard"""
        if current_user.role != 'admin':
            flash('Access denied.', 'error')
            return redirect(url_for('index'))
        
        # Get statistics
        stats = DatabaseOperations.get_dashboard_stats()
        risk_dist = DatabaseOperations.get_risk_distribution()
        
        # Get recent students
        recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
        
        # Get attendance statistics
        all_attendance = Attendance.query.all()
        avg_attendance = sum(a.attendance_percentage for a in all_attendance) / len(all_attendance) if all_attendance else 0
        
        return render_template(
            'dashboard.html',
            stats=stats,
            risk_distribution=risk_dist,
            recent_students=recent_students,
            avg_attendance=round(avg_attendance, 2)
        )
    
    # ==================== STUDENT MANAGEMENT ====================
    
    @app.route('/students', methods=['GET'])
    @login_required
    def students_list():
        """List all students"""
        if current_user.role not in ['admin', 'faculty']:
            flash('Access denied.', 'error')
            return redirect(url_for('index'))
        
        page = request.args.get('page', 1, type=int)
        pagination = DatabaseOperations.get_all_students(page=page, per_page=20)
        
        return render_template(
            'students.html',
            students=pagination.items,
            pagination=pagination
        )
    
    @app.route('/add_student', methods=['GET', 'POST'])
    @login_required
    def add_student():
        """Add new student"""
        if current_user.role != 'admin':
            flash('Only admins can add students.', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            # Get form data
            roll_number = request.form.get('roll_number', '').strip()
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '')
            gender = request.form.get('gender', '')
            city = request.form.get('city', '')
            state = request.form.get('state', '')
            
            # Validate required fields
            if not all([roll_number, first_name, last_name, email]):
                flash('All required fields must be filled.', 'error')
                return render_template('add_student.html')
            
            # Create student
            student, message = DatabaseOperations.create_student(
                roll_number=roll_number,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                gender=gender,
                city=city,
                state=state
            )
            
            if student:
                flash('Student added successfully.', 'success')
                return redirect(url_for('students_list'))
            else:
                flash(f'Error: {message}', 'error')
        
        return render_template('add_student.html')
    
    @app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
    @login_required
    def edit_student(student_id):
        """Edit student information"""
        if current_user.role != 'admin':
            flash('Only admins can edit students.', 'error')
            return redirect(url_for('index'))
        
        student = DatabaseOperations.get_student_by_id(student_id)
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('students_list'))
        
        if request.method == 'POST':
            # Get updated data
            update_data = {
                'first_name': request.form.get('first_name', '').strip(),
                'last_name': request.form.get('last_name', '').strip(),
                'email': request.form.get('email', '').strip(),
                'phone': request.form.get('phone', ''),
                'gender': request.form.get('gender', ''),
                'city': request.form.get('city', ''),
                'state': request.form.get('state', ''),
                'status': request.form.get('status', 'active')
            }
            
            # Update student
            updated_student, message = DatabaseOperations.update_student(student_id, **update_data)
            if updated_student:
                flash('Student updated successfully.', 'success')
                return redirect(url_for('students_list'))
            else:
                flash(f'Error: {message}', 'error')
        
        return render_template('edit_student.html', student=student)
    
    @app.route('/delete_student/<int:student_id>', methods=['GET'])
    @login_required
    def delete_student(student_id):
        """Delete student"""
        if current_user.role != 'admin':
            flash('Only admins can delete students.', 'error')
            return redirect(url_for('index'))
        
        success, message = DatabaseOperations.delete_student(student_id)
        if success:
            flash('Student deleted successfully.', 'success')
        else:
            flash(f'Error: {message}', 'error')
        
        return redirect(url_for('students_list'))
    
    # ==================== MARKS MANAGEMENT ====================
    
    @app.route('/add_marks/<int:student_id>', methods=['GET', 'POST'])
    @login_required
    def add_marks(student_id):
        """Add marks for student"""
        if current_user.role != 'admin':
            flash('Only admins can add marks.', 'error')
            return redirect(url_for('index'))
        
        student = DatabaseOperations.get_student_by_id(student_id)
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('students_list'))
        
        subjects = DatabaseOperations.get_all_subjects()
        
        if request.method == 'POST':
            subject_id = request.form.get('subject_id', type=int)
            internal_marks = request.form.get('internal_marks', type=float, default=0)
            assignment_marks = request.form.get('assignment_marks', type=float, default=0)
            practical_marks = request.form.get('practical_marks', type=float, default=0)
            external_marks = request.form.get('external_marks', type=float, default=0)
            exam_date = request.form.get('exam_date')
            
            # Validate marks
            if not (0 <= internal_marks <= 30 and 0 <= assignment_marks <= 10 and
                    0 <= practical_marks <= 20 and 0 <= external_marks <= 40):
                flash('Marks are out of valid range.', 'error')
                return render_template('add_marks.html', student=student, subjects=subjects)
            
            # Add marks
            mark, message = DatabaseOperations.add_marks(
                student_id=student_id,
                subject_id=subject_id,
                internal_marks=internal_marks,
                assignment_marks=assignment_marks,
                practical_marks=practical_marks,
                external_marks=external_marks,
                exam_date=exam_date
            )
            
            if mark:
                flash('Marks added successfully.', 'success')
                return redirect(url_for('student_details', student_id=student_id))
            else:
                flash(f'Error: {message}', 'error')
        
        return render_template('add_marks.html', student=student, subjects=subjects)
    
    # ==================== PREDICTIONS ====================
    
    @app.route('/predict', methods=['GET', 'POST'])
    @login_required
    def predict():
        """Prediction page"""
        if current_user.role not in ['admin', 'faculty']:
            flash('Access denied.', 'error')
            return redirect(url_for('index'))
        
        predictions_data = []
        
        if request.method == 'POST':
            # Get selected students (can be single or multiple)
            student_ids = request.form.getlist('student_ids')
            if not student_ids:
                flash('Please select at least one student.', 'error')
            else:
                # Load ML model
                try:
                    model = PredictionModel()
                    if not model.load_model():
                        flash('ML model not available. Please train the model first.', 'error')
                        return render_template('predict.html', students=Student.query.all())
                    
                    # Make predictions
                    for student_id in student_ids:
                        student = DatabaseOperations.get_student_by_id(int(student_id))
                        if student:
                            # Get student data
                            marks = DatabaseOperations.get_student_marks(student_id)
                            attendance_pct = DatabaseOperations.get_attendance_percentage(student_id)
                            cgpa = DatabaseOperations.get_student_cgpa(student_id)
                            
                            # Prepare features
                            if marks:
                                avg_internal = sum(m.internal_marks for m in marks) / len(marks)
                                avg_assignment = sum(m.assignment_marks for m in marks) / len(marks)
                                avg_practical = sum(m.practical_marks for m in marks) / len(marks)
                                avg_external = sum(m.external_marks for m in marks) / len(marks)
                            else:
                                avg_internal = avg_assignment = avg_practical = avg_external = 0
                            
                            features = {
                                'internal_marks': avg_internal,
                                'assignment_marks': avg_assignment,
                                'practical_marks': avg_practical,
                                'external_marks': avg_external,
                                'attendance': attendance_pct,
                                'num_subjects': len(marks) if marks else 0
                            }
                            
                            # Get prediction
                            try:
                                prediction = model.predict(features)
                                
                                # Save prediction
                                saved_pred, _ = DatabaseOperations.save_prediction(
                                    student_id=int(student_id),
                                    predicted_cgpa=prediction['predicted_cgpa'],
                                    risk_level=prediction['predicted_risk'],
                                    confidence=prediction['confidence'],
                                    probabilities=prediction['risk_probabilities'],
                                    features=features
                                )
                                
                                # Generate recommendations
                                DatabaseOperations.generate_recommendations(int(student_id))
                                
                                predictions_data.append({
                                    'student': student,
                                    'prediction': prediction,
                                    'cgpa': cgpa,
                                    'attendance': attendance_pct
                                })
                            except Exception as e:
                                flash(f'Prediction error for {student.roll_number}: {str(e)}', 'error')
                    
                    if predictions_data:
                        flash(f'Predictions completed for {len(predictions_data)} student(s).', 'success')
                
                except Exception as e:
                    flash(f'Error: {str(e)}', 'error')
        
        students = Student.query.all()
        return render_template('predict.html', students=students, predictions=predictions_data)
    
    @app.route('/api/predict', methods=['POST'])
    @login_required
    def api_predict():
        """API endpoint for prediction"""
        if current_user.role not in ['admin', 'faculty']:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        student_id = data.get('student_id')
        
        try:
            # Get student
            student = DatabaseOperations.get_student_by_id(student_id)
            if not student:
                return jsonify({'error': 'Student not found'}), 404
            
            # Load model and predict
            model = PredictionModel()
            if not model.load_model():
                return jsonify({'error': 'Model not available'}), 500
            
            # Prepare features
            marks = DatabaseOperations.get_student_marks(student_id)
            attendance_pct = DatabaseOperations.get_attendance_percentage(student_id)
            
            if marks:
                avg_internal = sum(m.internal_marks for m in marks) / len(marks)
                avg_assignment = sum(m.assignment_marks for m in marks) / len(marks)
                avg_practical = sum(m.practical_marks for m in marks) / len(marks)
                avg_external = sum(m.external_marks for m in marks) / len(marks)
            else:
                avg_internal = avg_assignment = avg_practical = avg_external = 0
            
            features = {
                'internal_marks': avg_internal,
                'assignment_marks': avg_assignment,
                'practical_marks': avg_practical,
                'external_marks': avg_external,
                'attendance': attendance_pct,
                'num_subjects': len(marks) if marks else 0
            }
            
            prediction = model.predict(features)
            
            return jsonify({
                'success': True,
                'prediction': prediction
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # ==================== REPORTS ====================
    
    @app.route('/reports', methods=['GET'])
    @login_required
    def reports():
        """Reports and analytics"""
        if current_user.role not in ['admin', 'faculty']:
            flash('Access denied.', 'error')
            return redirect(url_for('index'))
        
        # Get data for reports
        students = Student.query.all()
        
        # Calculate statistics
        stats = {
            'total_students': len(students),
            'active_students': len([s for s in students if s.status == 'active']),
            'avg_attendance': sum(DatabaseOperations.get_attendance_percentage(s.id) for s in students) / len(students) if students else 0,
        }
        
        # Get predictions
        predictions = Prediction.query.all()
        risk_counts = {
            'low': len([p for p in predictions if p.predicted_risk_level == 'Low']),
            'medium': len([p for p in predictions if p.predicted_risk_level == 'Medium']),
            'high': len([p for p in predictions if p.predicted_risk_level == 'High']),
        }
        
        return render_template(
            'reports.html',
            students=students,
            stats=stats,
            risk_counts=risk_counts
        )
    
    # ==================== FACULTY DASHBOARD ====================
    
    @app.route('/faculty_dashboard', methods=['GET'])
    @login_required
    def faculty_dashboard():
        """Faculty dashboard"""
        if current_user.role != 'faculty':
            flash('Access denied.', 'error')
            return redirect(url_for('index'))
        
        # Get students assigned to this faculty
        students = Student.query.filter_by(faculty_id=current_user.id).all()
        
        # Get statistics
        stats = {
            'total_students': len(students),
            'avg_attendance': sum(DatabaseOperations.get_attendance_percentage(s.id) for s in students) / len(students) if students else 0,
            'avg_cgpa': sum(DatabaseOperations.get_student_cgpa(s.id) for s in students) / len(students) if students else 0,
        }
        
        # Get high-risk students
        high_risk_students = []
        for student in students:
            prediction = DatabaseOperations.get_latest_prediction(student.id)
            if prediction and prediction.predicted_risk_level == 'High':
                high_risk_students.append(student)
        
        return render_template(
            'faculty_dashboard.html',
            students=students,
            stats=stats,
            high_risk_students=high_risk_students
        )
    
    # ==================== STUDENT DETAILS ====================
    
    @app.route('/student/<int:student_id>', methods=['GET'])
    @login_required
    def student_details(student_id):
        """Student details page"""
        student = DatabaseOperations.get_student_by_id(student_id)
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('students_list'))
        
        # Get student data
        marks = DatabaseOperations.get_student_marks(student_id)
        attendance_records = DatabaseOperations.get_student_attendance(student_id)
        cgpa = DatabaseOperations.get_student_cgpa(student_id)
        attendance_pct = DatabaseOperations.get_attendance_percentage(student_id)
        prediction = DatabaseOperations.get_latest_prediction(student_id)
        recommendations = DatabaseOperations.get_student_recommendations(student_id)
        
        return render_template(
            'student_details.html',
            student=student,
            marks=marks,
            attendance_records=attendance_records,
            cgpa=cgpa,
            attendance_pct=attendance_pct,
            prediction=prediction,
            recommendations=recommendations
        )
    
    # ==================== API ENDPOINTS ====================
    
    @app.route('/api/dashboard_stats', methods=['GET'])
    @login_required
    def api_dashboard_stats():
        """API endpoint for dashboard statistics"""
        if current_user.role != 'admin':
            return jsonify({'error': 'Access denied'}), 403
        
        stats = DatabaseOperations.get_dashboard_stats()
        risk_dist = DatabaseOperations.get_risk_distribution()
        
        return jsonify({
            'stats': stats,
            'risk_distribution': risk_dist
        })
    
    @app.route('/api/student_stats/<int:student_id>', methods=['GET'])
    @login_required
    def api_student_stats(student_id):
        """API endpoint for student statistics"""
        try:
            cgpa = DatabaseOperations.get_student_cgpa(student_id)
            attendance_pct = DatabaseOperations.get_attendance_percentage(student_id)
            marks = DatabaseOperations.get_student_marks(student_id)
            
            return jsonify({
                'cgpa': cgpa,
                'attendance': attendance_pct,
                'marks_count': len(marks)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/student_marks/<int:student_id>', methods=['GET'])
    @login_required
    def api_student_marks(student_id):
        """API endpoint for student marks"""
        try:
            marks = DatabaseOperations.get_student_marks(student_id)
            marks_data = [m.to_dict() for m in marks]
            return jsonify(marks_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == '__main__':
    # Create Flask app
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.environ.get('FLASK_ENV', 'development') == 'development'
    )
