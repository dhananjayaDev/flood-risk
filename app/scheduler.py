"""
Automatic River Height Data Collection Scheduler
Collects Kalu Ganga river height data every 30 minutes automatically
"""

import logging
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app import db
from app.river_height_manager import record_river_height, get_latest_river_height
from app.river import get_current_river_height

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiverDataScheduler:
    """
    Scheduler for automatic river height data collection
    """
    
    def __init__(self):
        self.scheduler = None
        self.is_running = False
        
    def start_scheduler(self):
        """Start the automatic data collection scheduler"""
        try:
            if self.is_running:
                logger.warning("Scheduler is already running")
                return False
            
            # Configure job store (SQLite database for persistence)
            jobstores = {
                'default': SQLAlchemyJobStore(url='sqlite:///scheduler_jobs.db')
            }
            
            # Configure executors
            executors = {
                'default': ThreadPoolExecutor(20),
            }
            
            # Configure job defaults
            job_defaults = {
                'coalesce': False,
                'max_instances': 1
            }
            
            # Create scheduler
            self.scheduler = BackgroundScheduler(
                jobstores=jobstores,
                executors=executors,
                job_defaults=job_defaults,
                timezone=pytz.timezone('Asia/Colombo')
            )
            
            # Add the river data collection job
            self.scheduler.add_job(
                func=self.collect_river_data,
                trigger=IntervalTrigger(minutes=30),  # Every 30 minutes
                id='river_data_collection',
                name='Kalu Ganga River Height Collection',
                replace_existing=True
            )
            
            # Start the scheduler
            self.scheduler.start()
            self.is_running = True
            
            logger.info("✅ River data collection scheduler started successfully")
            logger.info("📊 Collecting Kalu Ganga height every 30 minutes")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start scheduler: {e}")
            return False
    
    def stop_scheduler(self):
        """Stop the automatic data collection scheduler"""
        try:
            if not self.is_running or not self.scheduler:
                logger.warning("Scheduler is not running")
                return False
            
            self.scheduler.shutdown()
            self.is_running = False
            
            logger.info("⏹️ River data collection scheduler stopped")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to stop scheduler: {e}")
            return False
    
    def collect_river_data(self):
        """
        Collect and record river height data
        This function is called automatically every 30 minutes
        """
        try:
            logger.info("🔄 Starting automatic river data collection...")
            
            # Get current time for logging
            current_time = datetime.now(pytz.timezone('Asia/Colombo'))
            logger.info(f"⏰ Collection time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Try to get current river height from API
            try:
                current_data = get_current_river_height("Kalu Ganga (Ratnapura)")
                if current_data:
                    height = current_data['current_height']
                    api_timestamp = current_data['timestamp']
                    logger.info(f"📡 API data: {height}m at {api_timestamp}")
                else:
                    logger.warning("⚠️ No data from river API, using fallback")
                    height = None
                    api_timestamp = None
            except Exception as e:
                logger.warning(f"⚠️ River API error: {e}")
                height = None
                api_timestamp = None
            
            # Record the river height
            recorded = record_river_height(height=height, timestamp=api_timestamp)
            
            if recorded:
                logger.info(f"✅ Successfully recorded: {recorded.height}m at {recorded.timestamp}")
                
                # Get latest statistics
                latest = get_latest_river_height()
                if latest:
                    logger.info(f"📊 Latest recorded height: {latest.height}m")
                
                return True
            else:
                logger.error("❌ Failed to record river height data")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error in automatic data collection: {e}")
            return False
    
    def get_scheduler_status(self):
        """Get current scheduler status and job information"""
        try:
            if not self.scheduler or not self.is_running:
                return {
                    'status': 'stopped',
                    'jobs': [],
                    'next_run': None
                }
            
            jobs = self.scheduler.get_jobs()
            job_info = []
            
            for job in jobs:
                job_info.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else None,
                    'trigger': str(job.trigger)
                })
            
            return {
                'status': 'running' if self.is_running else 'stopped',
                'jobs': job_info,
                'next_run': job_info[0]['next_run_time'] if job_info else None
            }
            
        except Exception as e:
            logger.error(f"Error getting scheduler status: {e}")
            return {
                'status': 'error',
                'jobs': [],
                'next_run': None,
                'error': str(e)
            }
    
    def force_collect_now(self):
        """Manually trigger data collection (for testing)"""
        logger.info("🔧 Manual data collection triggered")
        return self.collect_river_data()

# Global scheduler instance
river_scheduler = RiverDataScheduler()

def start_automatic_collection():
    """Start automatic river data collection"""
    return river_scheduler.start_scheduler()

def stop_automatic_collection():
    """Stop automatic river data collection"""
    return river_scheduler.stop_scheduler()

def get_collection_status():
    """Get current collection status"""
    return river_scheduler.get_scheduler_status()

def collect_data_now():
    """Manually collect data now"""
    return river_scheduler.force_collect_now()

if __name__ == "__main__":
    # Test the scheduler
    print("Testing River Data Collection Scheduler...")
    
    # Start scheduler
    if start_automatic_collection():
        print("✅ Scheduler started successfully")
        
        # Show status
        status = get_collection_status()
        print(f"📊 Status: {status}")
        
        # Test manual collection
        print("🔧 Testing manual collection...")
        if collect_data_now():
            print("✅ Manual collection successful")
        else:
            print("❌ Manual collection failed")
        
        # Keep running for a bit to test
        import time
        print("⏳ Running for 2 minutes to test automatic collection...")
        time.sleep(120)  # 2 minutes
        
        # Stop scheduler
        if stop_automatic_collection():
            print("⏹️ Scheduler stopped successfully")
    else:
        print("❌ Failed to start scheduler")
