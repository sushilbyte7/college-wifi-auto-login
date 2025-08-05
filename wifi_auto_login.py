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
log_path = os.path.join(os.path.dirname(__file__), 'wifi_login.log')
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
MAX_LOGIN_ATTEMPTS = 3

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

def smart_wifi_handler():
    """Smart WiFi handler - runs only when login is needed"""
    logger.info("Starting Smart WiFi Auto-Login Handler...")
    
    # Check current WiFi
    wifi_name = get_connected_wifi_name()
    logger.info(f"Current WiFi: {wifi_name}")
    
    # If not connected to college WiFi, exit
    if wifi_name != COLLEGE_WIFI_NAME:
        logger.info(f"Not connected to {COLLEGE_WIFI_NAME}. Exiting.")
        return False
    
    logger.info(f"Connected to college WiFi: {COLLEGE_WIFI_NAME}")
    
    # Check if internet is already working
    if check_internet_connectivity():
        logger.info("Internet is already working! No login needed.")
        return True
    
    logger.info("No internet access detected. Starting login process...")
    
    # Check if portal is accessible
    if not is_portal_accessible():
        logger.error("Portal is not accessible. Cannot proceed with login.")
        return False
    
    # Attempt login with retries
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        logger.info(f"Login attempt {attempt}/{MAX_LOGIN_ATTEMPTS}")
        
        if login_to_wifi():
            # Wait for internet to stabilize
            logger.info("Login successful! Waiting for internet to stabilize...")
            time.sleep(5)
            
            # Verify internet connectivity
            if check_internet_connectivity():
                logger.info("✅ Internet connectivity confirmed! Login process completed.")
                return True
            else:
                logger.warning("Login appeared successful but internet still not working")
        
        if attempt < MAX_LOGIN_ATTEMPTS:
            wait_time = attempt * 2  # Progressive delay
            logger.info(f"Waiting {wait_time} seconds before next attempt...")
            time.sleep(wait_time)
    
    logger.error(f"All {MAX_LOGIN_ATTEMPTS} login attempts failed.")
    return False

def main():
    logger.info("="*50)
    logger.info("College WiFi Smart Auto-Login")
    logger.info("="*50)
    
    try:
        success = smart_wifi_handler()
        
        if success:
            logger.info("✅ WiFi login process completed successfully!")
            if len(sys.argv) <= 1 or sys.argv[1] != "--service":
                print("✅ Login successful! Script will now exit.")
        else:
            logger.error("❌ WiFi login process failed!")
            if len(sys.argv) <= 1 or sys.argv[1] != "--service":
                print("❌ Login failed! Check logs for details.")
                
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    logger.info("Script execution completed.")

if __name__ == "__main__":
    main()
