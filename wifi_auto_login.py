import subprocess
import socket
import time
import requests
from datetime import datetime
import configparser
import os
import sys

def log_error(msg):
    # Log errors to wifi_monitor.log only
    log_path = os.path.join(os.path.dirname(__file__), 'wifi_monitor.log')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [AUTO-LOGIN ERROR] {msg}\n")
    except:
        pass

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
except Exception as e:
    log_error(f"Error loading config: {e}, using defaults")

def get_connected_wifi_name():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except Exception as e:
        log_error(f"Error getting WiFi name: {e}")
    return None

def check_internet_connectivity():
    try:
        test_urls = [
            "http://www.google.com",
            "http://httpbin.org/ip",
            "http://www.msftconnecttest.com/connecttest.txt"
        ]
        for url in test_urls:
            try:
                response = requests.get(url, timeout=5, allow_redirects=False)
                if response.status_code == 302 or response.status_code == 301:
                    location = response.headers.get('Location', '')
                    if '10.11.200.1' in location or 'httpclient.html' in location:
                        return False
                elif response.status_code == 200:
                    if 'httpclient.html' not in response.text and '10.11.200.1' not in response.text:
                        return True
                    else:
                        return False
            except requests.exceptions.RequestException:
                continue
        return False
    except Exception as e:
        log_error(f"Internet connectivity check error: {e}")
    return False

def detect_captive_portal():
    try:
        response = requests.get("http://www.google.com", timeout=5, allow_redirects=False)
        if response.status_code in [302, 301, 307]:
            location = response.headers.get('Location', '')
            if '10.11.200.1' in location or 'httpclient.html' in location:
                return True
        try:
            portal_response = requests.get(PORTAL_URL, timeout=5)
            if portal_response.status_code == 200:
                return True
        except:
            pass
        return False
    except Exception as e:
        log_error(f"Captive portal detection error: {e}")
    return True  # Assume portal exists if we can't check

def is_portal_accessible():
    try:
        socket.create_connection(("10.11.200.1", 8090), timeout=5)
        return True
    except:
        return False

def login_to_wifi():
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
            return True
        else:
            return False
    except Exception as e:
        log_error(f"Login error: {e}")
    return False

def smart_wifi_handler():
    wifi_name = get_connected_wifi_name()
    if wifi_name != COLLEGE_WIFI_NAME:
        return False
    if check_internet_connectivity():
        return True
    if detect_captive_portal():
        pass
    else:
        pass
    if not is_portal_accessible():
        log_error("Portal is not accessible. Cannot proceed with login.")
        return False
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        if login_to_wifi():
            time.sleep(5)
            if check_internet_connectivity():
                return True
            else:
                log_error("Login appeared successful but internet still not working")
        if attempt < MAX_LOGIN_ATTEMPTS:
            wait_time = attempt * 2
            time.sleep(wait_time)
    log_error(f"All {MAX_LOGIN_ATTEMPTS} login attempts failed.")
    return False

def main():
    try:
        success = smart_wifi_handler()
        if success:
            if len(sys.argv) <= 1 or sys.argv[1] != "--service":
                print("✅ Login successful! Script will now exit.")
        else:
            log_error("WiFi login process failed!")
            if len(sys.argv) <= 1 or sys.argv[1] != "--service":
                print("❌ Login failed! Check logs for details.")
    except KeyboardInterrupt:
        log_error("Process interrupted by user")
    except Exception as e:
        log_error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
