"""JavaScript File - EduMind AI
Purpose: Frontend interactivity and dynamic updates
Author: EduMind AI Development Team
"""

// ============================================================
// SIDEBAR TOGGLE
// ============================================================

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// ============================================================
// FORM VALIDATION
// ============================================================

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const inputs = form.querySelectorAll('.form-control');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// ============================================================
// ALERT CLOSE
// ============================================================

function closeAlert(alertId) {
    const alert = document.getElementById(alertId);
    if (alert) {
        alert.style.display = 'none';
    }
}

// Auto-close alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert, index) => {
        const id = 'alert-' + index;
        alert.id = id;
        setTimeout(() => closeAlert(id), 5000);
    });
});

// ============================================================
// MODAL FUNCTIONALITY
// ============================================================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
});

// ============================================================
// TABLE SEARCH
// ============================================================

function searchTable(tableId, searchInputId) {
    const searchInput = document.getElementById(searchInputId);
    if (!searchInput) return;
    
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const searchTerm = searchInput.value.toLowerCase();
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// ============================================================
// DASHBOARD STATISTICS
// ============================================================

async function loadDashboardStats() {
    try {
        const response = await fetch('/api/dashboard_stats');
        const data = await response.json();
        
        if (data.stats) {
            updateStatCards(data.stats);
        }
        
        if (data.risk_distribution) {
            updateRiskChart(data.risk_distribution);
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

function updateStatCards(stats) {
    const elements = {
        'total-students': stats.total_students,
        'active-students': stats.active_students,
        'total-subjects': stats.total_subjects,
        'total-marks': stats.total_marks_records
    };
    
    Object.keys(elements).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = elements[id];
        }
    });
}

// ============================================================
// STUDENT PREDICTION
// ============================================================

async function predictStudent(studentId) {
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                student_id: studentId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showPredictionResult(data.prediction);
        } else {
            alert('Prediction error: ' + data.error);
        }
    } catch (error) {
        console.error('Error predicting student:', error);
        alert('Error making prediction');
    }
}

function showPredictionResult(prediction) {
    const resultHtml = `
        <div class="alert alert-info">
            <strong>Prediction Result</strong>
            <p>Predicted CGPA: ${prediction.predicted_cgpa.toFixed(2)}</p>
            <p>Risk Level: ${prediction.predicted_risk}</p>
            <p>Confidence: ${(prediction.confidence * 100).toFixed(2)}%</p>
        </div>
    `;
    
    const container = document.getElementById('prediction-result');
    if (container) {
        container.innerHTML = resultHtml;
    }
}

// ============================================================
// CHART.JS INTEGRATION
// ============================================================

// Risk Distribution Chart
function initRiskChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk', 'Medium Risk', 'High Risk'],
            datasets: [{
                data: [data.low, data.medium, data.high],
                backgroundColor: ['#27ae60', '#f39c12', '#e74c3c'],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Attendance Chart
function initAttendanceChart(canvasId, attendanceData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: attendanceData.labels,
            datasets: [{
                label: 'Attendance %',
                data: attendanceData.values,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Marks Chart
function initMarksChart(canvasId, marksData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: marksData.subjects,
            datasets: [{
                label: 'Total Marks',
                data: marksData.values,
                backgroundColor: [
                    '#3498db', '#e74c3c', '#27ae60',
                    '#f39c12', '#9b59b6', '#1abc9c'
                ],
                borderWidth: 1,
                borderColor: '#ddd'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// ============================================================
// FORM SUBMISSION
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// ============================================================
// DYNAMIC TABLE UPDATE
// ============================================================

async function loadStudentMarks(studentId) {
    try {
        const response = await fetch(`/api/student_marks/${studentId}`);
        const marks = await response.json();
        
        let html = '';
        marks.forEach(mark => {
            html += `
                <tr>
                    <td>${mark.subject}</td>
                    <td>${mark.internal_marks}</td>
                    <td>${mark.assignment_marks}</td>
                    <td>${mark.practical_marks}</td>
                    <td>${mark.external_marks}</td>
                    <td><strong>${mark.total_marks}</strong></td>
                    <td><span class="badge badge-primary">${mark.grade}</span></td>
                </tr>
            `;
        });
        
        const tbody = document.getElementById('marks-table-body');
        if (tbody) {
            tbody.innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading marks:', error);
    }
}

// ============================================================
// DELETE CONFIRMATION
// ============================================================

function confirmDelete(message = 'Are you sure you want to delete this record?') {
    return confirm(message);
}

// ============================================================
// DATE PICKER
// ============================================================

function initDatePicker(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.type = 'date';
    }
}

// ============================================================
// PAGINATION
// ============================================================

function goToPage(pageNumber) {
    const url = new URL(window.location);
    url.searchParams.set('page', pageNumber);
    window.location = url.toString();
}

// ============================================================
// UTILITIES
// ============================================================

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(value);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Show loading spinner
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';
    }
}

// Hide loading spinner
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}
