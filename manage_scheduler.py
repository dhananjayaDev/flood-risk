"""
River Data Collection Scheduler Management
Simple script to start, stop, and monitor the automatic data collection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.scheduler import start_automatic_collection, stop_automatic_collection, get_collection_status, collect_data_now

def show_status():
    """Show current scheduler status"""
    print("=== River Data Collection Status ===")
    status = get_collection_status()
    
    print(f"Status: {status['status'].upper()}")
    print(f"Next Collection: {status['next_run'] or 'Not scheduled'}")
    
    if status['jobs']:
        print("\nScheduled Jobs:")
        for job in status['jobs']:
            print(f"  - {job['name']}: {job['next_run_time'] or 'Not scheduled'}")
    
    if 'error' in status:
        print(f"\nError: {status['error']}")

def start_collection():
    """Start automatic data collection"""
    print("Starting automatic river data collection...")
    if start_automatic_collection():
        print("✅ Automatic collection started successfully")
        show_status()
    else:
        print("❌ Failed to start automatic collection")

def stop_collection():
    """Stop automatic data collection"""
    print("Stopping automatic river data collection...")
    if stop_automatic_collection():
        print("✅ Automatic collection stopped successfully")
    else:
        print("❌ Failed to stop automatic collection")

def collect_now():
    """Manually collect data now"""
    print("Manually collecting river data...")
    if collect_data_now():
        print("✅ Manual collection completed successfully")
    else:
        print("❌ Manual collection failed")

def main():
    """Main management interface"""
    if len(sys.argv) < 2:
        print("River Data Collection Scheduler Manager")
        print("Usage:")
        print("  python manage_scheduler.py start    - Start automatic collection")
        print("  python manage_scheduler.py stop     - Stop automatic collection")
        print("  python manage_scheduler.py status   - Show current status")
        print("  python manage_scheduler.py collect  - Collect data now")
        return
    
    command = sys.argv[1].lower()
    
    # Create app context
    app = create_app()
    with app.app_context():
        if command == 'start':
            start_collection()
        elif command == 'stop':
            stop_collection()
        elif command == 'status':
            show_status()
        elif command == 'collect':
            collect_now()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: start, stop, status, collect")

if __name__ == "__main__":
    main()
