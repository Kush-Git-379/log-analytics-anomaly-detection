import pandas as pd
import sys
import smtplib
from email.message import EmailMessage
from datetime import datetime

# --- CONFIGURATION ---
# Replace these with your actual details
EMAIL_SENDER = "kushkm2604@gmail.com"
EMAIL_APP_PASSWORD = "fbzh dful kisy rgiy" 
EMAIL_RECEIVER = "kushkm2604@gmail.com" # Can be the same as sender
ALERT_LOG_FILE = "alerts.log"
DATA_FILE = "system_health.csv"

# --- HELPER FUNCTIONS ---
def write_to_log(message):
    """Appends an alert message to a local text file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ALERT_LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def send_email_alert(subject, body):
    """Sends an email notification via Gmail's SMTP server."""
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        # Connect to Gmail's secure SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("�� Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# --- MAIN LOGIC ---
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"Error: {DATA_FILE} not found. Run the shell script first!")
    sys.exit()

# Calculate dynamic threshold
cpu_mean = df['CPU_Percent'].mean()
cpu_std = df['CPU_Percent'].std()
cpu_threshold = cpu_mean + (2 * cpu_std)

if cpu_threshold < 10: 
    cpu_threshold = 50.0

latest = df.iloc[-1]
current_cpu = latest['CPU_Percent']
timestamp = latest['Timestamp']

print(f"\n--- SYSTEM HEALTH REPORT : {timestamp} ---")
print(f"Current CPU: {current_cpu}% (Threshold: {cpu_threshold:.2f}%)")

# --- ANOMALY DETECTION & ALERTING ---
if current_cpu > cpu_threshold:
    alert_msg = f"ANOMALY DETECTED: CPU Usage spiked to {current_cpu}% (Threshold was {cpu_threshold:.2f}%)"
    print(f"⚠️  {alert_msg}")
    
    # 1. Write to the local log file
    write_to_log(alert_msg)
    
    # 2. Send the email
    send_email_alert("�� System Alert: High CPU Usage", alert_msg)
    
elif current_cpu > 80:
    alert_msg = f"CRITICAL WARNING: CPU Usage is dangerously high at {current_cpu}%!"
    print(f"⚠️  {alert_msg}")
    write_to_log(alert_msg)
    send_email_alert("�� System Alert: CRITICAL CPU Usage", alert_msg)
    
else:
    print("✅  System Status: NORMAL")

print("-" * 40)

print("-" * 40)
