import subprocess
import socket
import time
import requests
import threading
from datetime import datetime
import configparser
import os

# Load configuration
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

# ---- CONFIGURATION ----
# Default values (will be overridden by config.ini if it exists)
COLLEGE_WIFI_NAME = "PCU_Student"
PORTAL_URL = "http://10.11.200.1:8090/httpclient.html"
LOGIN_URL = "http://10.11.200.1:8090/login.xml"
USERNAME = "comp1"
PASSWORD = "Pcu@123456"
CHECK_INTERVAL = 30  # Check every 30 seconds

# Try to load from config file
try:
    if os.path.exists(config_path):
        config.read(config_path)
        COLLEGE_WIFI_NAME = config.get('WIFI_SETTINGS', 'COLLEGE_WIFI_NAME', fallback=COLLEGE_WIFI_NAME)
        PORTAL_URL = config.get('WIFI_SETTINGS', 'PORTAL_URL', fallback=PORTAL_URL)
        LOGIN_URL = config.get('WIFI_SETTINGS', 'LOGIN_URL', fallback=LOGIN_URL)
        USERNAME = config.get('CREDENTIALS', 'USERNAME', fallback=USERNAME)
        PASSWORD = config.get('CREDENTIALS', 'PASSWORD', fallback=PASSWORD)
        CHECK_INTERVAL = config.getint('MONITORING', 'CHECK_INTERVAL', fallback=CHECK_INTERVAL)
        print("✅ Configuration loaded from config.ini")
    else:
        print("⚠️ config.ini not found, using default settings")
except Exception as e:
    print(f"⚠️ Error loading config: {e}, using default settings")
# ------------------------

def get_connected_wifi_name():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f"❌ Error getting WiFi name: {e}")
        return None

def is_portal_accessible():
    try:
        # Check if we can reach the portal
        socket.create_connection(("10.11.200.1", 8090), timeout=5)
        return True
    except Exception as e:
        print(f"❌ Portal not accessible: {e}")
        return False

def check_internet_connectivity():
    """Check if we have internet access by trying to reach a reliable server"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False

def get_portal_page():
    """Fetch the portal page to understand its structure"""
    try:
        response = requests.get(PORTAL_URL, timeout=10)
        return response.text
    except Exception as e:
        print(f"❌ Error fetching portal page: {e}")
        return None

def login_to_wifi():
    """Attempt to login to the WiFi portal"""
    print("🔐 Attempting to login...")
    
    # First, let's check the portal structure
    portal_content = get_portal_page()
    if portal_content:
        print("📄 Portal page accessible")
    
    # Try the original login method
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
        print(f"📡 Login response status: {response.status_code}")
        
        if "LIVE" in response.text or response.status_code == 200:
            print("✅ Login successful!")
            return True
        else:
            print(f"⚠️ Login response: {response.text[:200]}...")
            
            # Try alternative login methods if the first one fails
            return try_alternative_login()
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return try_alternative_login()

def try_alternative_login():
    """Try alternative login methods"""
    print("🔄 Trying alternative login methods...")
    
    # Method 2: Try with different payload structure
    alt_payloads = [
        {
            "username": USERNAME,
            "password": PASSWORD,
            "login": "Login"
        },
        {
            "user": USERNAME,
            "pass": PASSWORD,
            "action": "login"
        },
        {
            "userid": USERNAME,
            "pwd": PASSWORD,
            "submit": "Login"
        }
    ]
    
    for i, payload in enumerate(alt_payloads, 1):
        try:
            print(f"🔄 Trying method {i}...")
            response = requests.post(LOGIN_URL, data=payload, timeout=10)
            if response.status_code == 200 and ("success" in response.text.lower() or "live" in response.text.lower()):
                print(f"✅ Alternative login method {i} successful!")
                return True
        except Exception as e:
            print(f"❌ Method {i} failed: {e}")
    
    return False

def monitor_and_login():
    """Continuously monitor WiFi and login when needed"""
    print("🚀 Starting WiFi auto-login monitor...")
    print(f"📡 Monitoring for WiFi: {COLLEGE_WIFI_NAME}")
    print(f"⏰ Check interval: {CHECK_INTERVAL} seconds")
    print("💡 Will reduce frequency when internet is stable")
    print("Press Ctrl+C to stop monitoring\n")
    
    last_wifi = None
    internet_stable_count = 0
    
    while True:
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            wifi_name = get_connected_wifi_name()
            
            # Check if WiFi changed
            if wifi_name != last_wifi:
                print(f"[{current_time}] 📶 WiFi changed: {last_wifi} → {wifi_name}")
                last_wifi = wifi_name
                internet_stable_count = 0
            
            if wifi_name == COLLEGE_WIFI_NAME:
                # Check if we already have internet
                if check_internet_connectivity():
                    internet_stable_count += 1
                    if internet_stable_count == 1:
                        print(f"[{current_time}] ✅ Internet is working")
                    elif internet_stable_count == 5:
                        print(f"[{current_time}] 😴 Internet stable, reducing check frequency...")
                    
                    # If internet is stable for 5+ checks, check less frequently
                    if internet_stable_count >= 5:
                        time.sleep(CHECK_INTERVAL * 3)  # Check every 90 seconds
                        continue
                        
                else:
                    print(f"[{current_time}] 🔐 No internet access, attempting login...")
                    internet_stable_count = 0
                    
                    if is_portal_accessible():
                        login_success = login_to_wifi()
                        if login_success:
                            print(f"[{current_time}] 🎉 Successfully logged in!")
                            # Wait a moment and verify internet
                            time.sleep(3)
                            if check_internet_connectivity():
                                print(f"[{current_time}] ✅ Internet confirmed working!")
                        else:
                            print(f"[{current_time}] ❌ Login failed, will retry in {CHECK_INTERVAL} seconds")
                    else:
                        print(f"[{current_time}] ❌ Portal not accessible")
            else:
                print(f"[{current_time}] 📱 Connected to: {wifi_name or 'None'} (not college WiFi)")
                internet_stable_count = 0
                # Sleep longer when not on college WiFi
                time.sleep(CHECK_INTERVAL * 2)
                continue
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            time.sleep(CHECK_INTERVAL)

def main():
    print("🎓 College WiFi Auto-Login System")
    print("="*50)
    
    # Check current status
    wifi = get_connected_wifi_name()
    print(f"📡 Current WiFi: {wifi or 'None'}")
    
    if wifi == COLLEGE_WIFI_NAME:
        print(f"✅ Connected to college WiFi: {COLLEGE_WIFI_NAME}")
        
        # Check internet connectivity
        if check_internet_connectivity():
            print("🌐 Internet is already working!")
            choice = input("\n🤔 Do you want to start monitoring anyway? (y/n): ").lower()
            if choice != 'y':
                return
        else:
            print("🔐 No internet access detected")
            if is_portal_accessible():
                print("🚪 Portal is accessible, attempting login...")
                login_to_wifi()
            else:
                print("❌ Portal not accessible")
    else:
        print(f"⚠️ Not connected to college WiFi ({COLLEGE_WIFI_NAME})")
        print("📶 Please connect to the college WiFi first")
    
    # Ask if user wants to start monitoring
    print(f"\n🔄 Do you want to start automatic monitoring?")
    print(f"   This will check every {CHECK_INTERVAL} seconds and auto-login when needed.")
    choice = input("Start monitoring? (y/n): ").lower()
    
    if choice == 'y':
        monitor_and_login()
    else:
        print("👋 Exiting...")

if __name__ == "__main__":
    main()
