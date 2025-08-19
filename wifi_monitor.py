import subprocess
import time
import os
import sys
from datetime import datetime

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUTO_LOGIN_SCRIPT = os.path.join(SCRIPT_DIR, "wifi_auto_login.py")
LOG_FILE = os.path.join(SCRIPT_DIR, "wifi_monitor.log")
LOG_DATE_FILE = os.path.join(SCRIPT_DIR, ".last_log_date")

def check_and_rotate_log():
    """Check if we need to rotate/reset the log file daily or if it's too large"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check if we have a stored date
        last_date = ""
        if os.path.exists(LOG_DATE_FILE):
            with open(LOG_DATE_FILE, "r") as f:
                last_date = f.read().strip()
        
        # Check log file size (if > 5MB, force rotation)
        log_too_large = False
        if os.path.exists(LOG_FILE):
            file_size = os.path.getsize(LOG_FILE)
            if file_size > 5 * 1024 * 1024:  # 5MB
                log_too_large = True
        
        # If date changed or log too large, clear the log
        if last_date != today or log_too_large:
            # Clear old log
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                rotation_reason = "Daily" if last_date != today else "Size Limit"
                f.write(f"=== WiFi Monitor Log Started: {today} ({rotation_reason} Rotation) ===\n")
            
            # Update date file
            with open(LOG_DATE_FILE, "w") as f:
                f.write(today)
                
            return True  # Log was rotated
        return False  # No rotation needed
        
    except Exception as e:
        # If anything fails, just continue
        return False

def log_message(message):
    """Log message to file and console with daily rotation"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    try:
        # Check if we need to rotate log first
        check_and_rotate_log()
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except:
        pass

def get_connected_wifi():
    """Get currently connected WiFi name"""
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except:
        return None

def run_auto_login():
    """Run the auto-login script"""
    try:
        log_message("🔐 Running auto-login script...")
        result = subprocess.run([sys.executable, AUTO_LOGIN_SCRIPT, "--service"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            log_message("✅ Auto-login script completed successfully")
        else:
            log_message(f"⚠️ Auto-login script returned code {result.returncode}")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        log_message("⏰ Auto-login script timed out")
        return False
    except Exception as e:
        log_message(f"❌ Error running auto-login script: {e}")
        return False

def wifi_connection_monitor():
    """Monitor WiFi connection changes and trigger login when needed"""
    log_message("🚀 Starting WiFi Connection Monitor...")
    log_message("📡 Monitoring for college WiFi connections...")
    
    last_wifi = None
    college_wifi_name = "PCU_Student"
    
    while True:
        try:
            current_wifi = get_connected_wifi()
            
            # Check if WiFi changed
            if current_wifi != last_wifi:
                log_message(f"📶 WiFi changed: '{last_wifi}' → '{current_wifi}'")
                last_wifi = current_wifi
                
                # If connected to college WiFi, trigger auto-login
                if current_wifi == college_wifi_name:
                    log_message(f"🎓 Connected to college WiFi: {college_wifi_name}")
                    log_message("🔄 Triggering auto-login process...")
                    
                    success = run_auto_login()
                    
                    if success:
                        log_message("✅ Auto-login process completed successfully!")
                    else:
                        log_message("❌ Auto-login process failed!")
                
                elif current_wifi:
                    log_message(f"📱 Connected to: {current_wifi} (not college WiFi)")
                else:
                    log_message("📵 No WiFi connection detected")
            
            # Sleep for a while before next check
            time.sleep(10)  # Check every 10 seconds for WiFi changes
            
        except KeyboardInterrupt:
            log_message("🛑 Monitor stopped by user")
            break
        except Exception as e:
            log_message(f"❌ Monitor error: {e}")
            time.sleep(30)  # Wait longer on error

def main():
    log_message("="*60)
    log_message("College WiFi Connection Monitor")
    log_message("="*60)
    log_message("This monitors WiFi connections and auto-login when needed")
    log_message("Script will run once per WiFi connection to college network")
    log_message("Press Ctrl+C to stop")
    log_message("")
    
    try:
        wifi_connection_monitor()
    except KeyboardInterrupt:
        log_message("Monitor stopped by user")

if __name__ == "__main__":
    main()
