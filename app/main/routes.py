from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import emit
from app.main import bp
from app import socketio
import random
from datetime import datetime, timedelta

@bp.route('/')
@bp.route('/index')
def index():
    # Redirect to signin page if user is not authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    # If authenticated, redirect to dashboard
    return redirect(url_for('main.home'))

@bp.route('/landing')
def landing():
    """Public landing page for marketing/information purposes"""
    return render_template('index.html', title='Home')

@bp.route('/home')
@login_required
def home():
    # Generate dynamic dashboard data
    dashboard_data = {
        'stats': {
            'active_sensors': random.randint(8, 15),
            'alerts': random.randint(1, 5),
            'system_uptime': round(random.uniform(95, 99.9), 1),
            'monitored_areas': random.randint(3, 8)
        },
        'recent_alerts': [
            {
                'id': 1,
                'severity': 'high',
                'icon': 'fas fa-exclamation-triangle',
                'color': 'text-danger',
                'title': 'High Water Level Detected',
                'description': 'Sensor A-1 detected rising water levels above threshold',
                'location': 'River Station A-1',
                'timestamp': datetime.now() - timedelta(minutes=2),
                'risk_probability': 85
            },
            {
                'id': 2,
                'severity': 'medium',
                'icon': 'fas fa-exclamation-circle',
                'color': 'text-warning',
                'title': 'Soil Moisture Alert',
                'description': 'Excessive soil moisture detected in monitoring zone B',
                'location': 'Zone B-3',
                'timestamp': datetime.now() - timedelta(minutes=15),
                'risk_probability': 65
            },
            {
                'id': 3,
                'severity': 'low',
                'icon': 'fas fa-info-circle',
                'color': 'text-info',
                'title': 'System Maintenance',
                'description': 'Scheduled maintenance completed on sensor C-2',
                'location': 'Sensor C-2',
                'timestamp': datetime.now() - timedelta(hours=1),
                'risk_probability': 0
            }
        ],
        'recent_notifications': [
            {
                'id': 1,
                'type': 'email',
                'icon': 'fas fa-envelope',
                'color': 'text-primary',
                'message': 'Flood alert sent to residents in Zone A',
                'recipients': 45,
                'timestamp': datetime.now() - timedelta(minutes=5)
            },
            {
                'id': 2,
                'type': 'sms',
                'icon': 'fas fa-sms',
                'color': 'text-success',
                'message': 'SMS notification sent to emergency contacts',
                'recipients': 12,
                'timestamp': datetime.now() - timedelta(minutes=10)
            },
            {
                'id': 3,
                'type': 'ivr',
                'icon': 'fas fa-phone',
                'color': 'text-warning',
                'message': 'Automated call made to Zone B residents',
                'recipients': 23,
                'timestamp': datetime.now() - timedelta(minutes=20)
            }
        ],
        'sensor_data': {
            'rainfall': [random.uniform(0, 50) for _ in range(24)],
            'soil_moisture': [random.uniform(20, 80) for _ in range(24)],
            'groundwater': [random.uniform(10, 90) for _ in range(24)],
            'timestamps': [(datetime.now() - timedelta(hours=i)).strftime('%H:%M') for i in range(23, -1, -1)]
        },
        'map_data': {
            'sensors': [
                {
                    'id': 'A-1',
                    'type': 'rainfall',
                    'lat': 40.7128,
                    'lng': -74.0060,
                    'reading': 45.2,
                    'risk_level': 'high',
                    'last_update': datetime.now() - timedelta(minutes=2)
                },
                {
                    'id': 'B-2',
                    'type': 'soil_moisture',
                    'lat': 40.7589,
                    'lng': -73.9851,
                    'reading': 78.5,
                    'risk_level': 'medium',
                    'last_update': datetime.now() - timedelta(minutes=5)
                },
                {
                    'id': 'C-3',
                    'type': 'tilt',
                    'lat': 40.7505,
                    'lng': -73.9934,
                    'reading': 2.1,
                    'risk_level': 'low',
                    'last_update': datetime.now() - timedelta(minutes=1)
                },
                {
                    'id': 'D-4',
                    'type': 'river_level',
                    'lat': 40.6892,
                    'lng': -74.0445,
                    'reading': 12.8,
                    'risk_level': 'high',
                    'last_update': datetime.now() - timedelta(minutes=3)
                }
            ],
            'risk_zones': [
                {'lat': 40.7128, 'lng': -74.0060, 'risk': 'high', 'name': 'Zone A'},
                {'lat': 40.7589, 'lng': -73.9851, 'risk': 'medium', 'name': 'Zone B'},
                {'lat': 40.7505, 'lng': -73.9934, 'risk': 'low', 'name': 'Zone C'},
                {'lat': 40.6892, 'lng': -74.0445, 'risk': 'high', 'name': 'Zone D'}
            ]
        }
    }
    
    return render_template('home.html', title='Dashboard', user=current_user, data=dashboard_data)

# SocketIO Event Handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'msg': 'Connected to flood monitoring system'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_data')
def handle_data_request():
    # Simulate real-time data updates
    import threading
    import time
    
    def send_updates():
        while True:
            time.sleep(30)  # Send updates every 30 seconds
            # Simulate new sensor reading
            new_reading = {
                'sensor_id': f'S-{random.randint(1, 10)}',
                'type': random.choice(['rainfall', 'soil_moisture', 'tilt', 'river_level']),
                'value': round(random.uniform(0, 100), 1),
                'timestamp': datetime.now().isoformat(),
                'risk_level': random.choice(['low', 'medium', 'high'])
            }
            socketio.emit('reading:new', new_reading)
            
            # Simulate new alert occasionally
            if random.random() < 0.1:  # 10% chance
                new_alert = {
                    'id': random.randint(1000, 9999),
                    'severity': random.choice(['low', 'medium', 'high']),
                    'title': f'Alert from Sensor {new_reading["sensor_id"]}',
                    'description': f'Unusual reading detected: {new_reading["value"]}',
                    'location': f'Zone {random.choice(["A", "B", "C", "D"])}',
                    'timestamp': datetime.now().isoformat(),
                    'risk_probability': random.randint(20, 90)
                }
                socketio.emit('alert:opened', new_alert)
    
    # Start background thread for updates
    thread = threading.Thread(target=send_updates)
    thread.daemon = True
    thread.start()
