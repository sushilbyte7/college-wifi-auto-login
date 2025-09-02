import subprocess
import socket
import time
import requests
from datetime import datetime
import configparser
import os
import sys
import logging

# Set up logging
log_path = None
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Load configuration
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

# Default configuration
COLLEGE_WIFI_NAME = "PCU_Student"
PORTAL_URL = "http://10.11.200.1:8090/httpclient.html"
LOGIN_URL = "http://10.11.200.1:8090/login.xml"
USERNAME = "comp1"
PASSWORD = "Pcu@123456"
CHECK_INTERVAL = 30

# Load from config file
try:
    if os.path.exists(config_path):
        config.read(config_path)
        COLLEGE_WIFI_NAME = config.get('WIFI_SETTINGS', 'COLLEGE_WIFI_NAME', fallback=COLLEGE_WIFI_NAME)
        PORTAL_URL = config.get('WIFI_SETTINGS', 'PORTAL_URL', fallback=PORTAL_URL)
        LOGIN_URL = config.get('WIFI_SETTINGS', 'LOGIN_URL', fallback=LOGIN_URL)
        USERNAME = config.get('CREDENTIALS', 'USERNAME', fallback=USERNAME)
        PASSWORD = config.get('CREDENTIALS', 'PASSWORD', fallback=PASSWORD)
        CHECK_INTERVAL = config.getint('MONITORING', 'CHECK_INTERVAL', fallback=CHECK_INTERVAL)
        logger.info("Configuration loaded from config.ini")
except Exception as e:
    logger.warning(f"Error loading config: {e}, using defaults")

def get_connected_wifi_name():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except Exception as e:
        logger.error(f"Error getting WiFi name: {e}")
        return None

def check_internet_connectivity():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False

def is_portal_accessible():
    try:
        socket.create_connection(("10.11.200.1", 8090), timeout=5)
        return True
    except:
        return False

def login_to_wifi():
    logger.info("Attempting WiFi login...")
    
    payload = {
        "mode": "191",
        "username": USERNAME,
        "password": PASSWORD,
        "a": int(time.time() * 1000)
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': PORTAL_URL,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(LOGIN_URL, data=payload, headers=headers, timeout=10)
        
        if "LIVE" in response.text or response.status_code == 200:
            logger.info("Login successful!")
            return True
        else:
            logger.warning(f"Login failed. Response: {response.text[:100]}...")
            return False
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return False

def main_loop():
    logger.info("Starting WiFi auto-login service...")
    logger.info(f"Monitoring WiFi: {COLLEGE_WIFI_NAME}")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    
    consecutive_failures = 0
    max_failures = 5
    last_wifi = None
    internet_was_working = False
    idle_count = 0
    max_idle_checks = 10  # After 10 successful checks, reduce frequency
    
    while True:
        try:
            wifi_name = get_connected_wifi_name()
            
            # Check if WiFi changed
            if wifi_name != last_wifi:
                logger.info(f"WiFi changed from '{last_wifi}' to '{wifi_name}'")
                last_wifi = wifi_name
                internet_was_working = False
                idle_count = 0
            
            if wifi_name == COLLEGE_WIFI_NAME:
                internet_working = check_internet_connectivity()
                
                if not internet_working:
                    logger.info("No internet access detected, attempting login...")
                    internet_was_working = False
                    idle_count = 0
                    
                    if is_portal_accessible():
                        if login_to_wifi():
                            logger.info("Successfully logged in!")
                            consecutive_failures = 0
                            # Give some time for internet to stabilize
                            time.sleep(5)
                            if check_internet_connectivity():
                                logger.info("Internet connectivity confirmed!")
                                internet_was_working = True
                        else:
                            consecutive_failures += 1
                            logger.warning(f"Login attempt failed ({consecutive_failures}/{max_failures})")
                    else:
                        logger.warning("Portal not accessible")
                        consecutive_failures += 1
                        
                else:
                    # Internet is working
                    if not internet_was_working:
                        logger.info("Internet connectivity restored/confirmed")
                        internet_was_working = True
                        consecutive_failures = 0
                        idle_count = 0
                    else:
                        idle_count += 1
                        
                    # If internet has been working for a while, check less frequently
                    if idle_count >= max_idle_checks:
                        logger.info(f"Internet stable for {idle_count} checks, reducing monitoring frequency")
                        time.sleep(CHECK_INTERVAL * 3)  # Check every 90 seconds instead of 30
                        idle_count = max_idle_checks  # Keep it at max to continue slow checking
                        continue
            else:
                # Not connected to college WiFi
                if last_wifi != wifi_name and wifi_name:
                    logger.info(f"Connected to different WiFi: {wifi_name}")
                internet_was_working = False
                idle_count = 0
                
                # If not on college WiFi, check less frequently
                time.sleep(CHECK_INTERVAL * 2)
                continue
            
            # Calculate sleep time based on failures
            if consecutive_failures > 0:
                sleep_time = CHECK_INTERVAL * (2 ** min(consecutive_failures, 3))
                logger.info(f"Sleeping for {sleep_time}s due to {consecutive_failures} failures")
            else:
                sleep_time = CHECK_INTERVAL
                
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            logger.info("Service stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            consecutive_failures += 1
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--service":
        # Run as service (no interactive prompts)
        main_loop()
    else:
        # Interactive mode
        print("🎓 College WiFi Auto-Login Service")
        print("This will run continuously in the background")
        print("Press Ctrl+C to stop")
        print(f"Log file: {log_path}")
        print()
        
        try:
            main_loop()
        except KeyboardInterrupt:
            print("\nService stopped.")
