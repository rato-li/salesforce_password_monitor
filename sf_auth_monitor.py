import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import configparser
import json

class SalesforceAuthMonitor:
    def __init__(self):
        self.config = self._load_config()
        self.alert_recipients = self.config['ALERT_SETTINGS']['recipients'].split(',')
        
    def _load_config(self):
        config = configparser.ConfigParser()
        config.read('salesforce_config.ini')
        return config
    
    def check_password_expiry(self):
        """Check password expiry using Salesforce REST API"""
        try:
            auth_url = f"https://{self.config['SALESFORCE']['domain']}.salesforce.com/services/oauth2/token"
            payload = {
                'grant_type': 'password',
                'client_id': self.config['SALESFORCE']['client_id'],
                'client_secret': self.config['SALESFORCE']['client_secret'],
                'username': self.config['SALESFORCE']['username'],
                'password': self.config['SALESFORCE']['password'] + self.config['SALESFORCE']['security_token']
            }
            
            response = requests.post(auth_url, data=payload)
            response_data = response.json()
            
            if response.status_code == 400:
                error_desc = response_data.get('error_description', '')
                if 'password expired' in error_desc.lower():
                    self._send_alert("CRITICAL: Salesforce password has expired", 
                                    f"Password for {self.config['SALESFORCE']['username']} has expired. Immediate action required.")
                    return True
                elif 'invalid grant' in error_desc.lower():
                    self._send_alert("WARNING: Salesforce authentication failure", 
                                    "Potential security token invalidation or password change detected.")
                    return True
            return False
            
        except Exception as e:
            self._send_alert("ERROR: Salesforce connection failure", 
                           f"Exception occurred while checking password status: {str(e)}")
            return False
    
    def _send_alert(self, subject, message):
        """Send alert via email and logging system"""
        # Email notification
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.config['ALERT_SETTINGS']['sender_email']
        msg['To'] = ", ".join(self.alert_recipients)
        
        try:
            with smtplib.SMTP(self.config['ALERT_SETTINGS']['smtp_server'], 
                             int(self.config['ALERT_SETTINGS']['smtp_port'])) as server:
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email alert: {str(e)}")
        
        # Log to monitoring system (e.g., Splunk, Datadog)
        self._log_alert(subject, message)
    
    def _log_alert(self, severity, message):
        """Log alerts to monitoring system"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "system": "Salesforce DataLoader",
            "severity": severity.split(':')[0].strip(),
            "message": message
        }
        # Implement your preferred logging mechanism here
        print(json.dumps(log_entry))  # Replace with actual logging

if __name__ == "__main__":
    monitor = SalesforceAuthMonitor()
    if monitor.check_password_expiry():
        print("Alert sent for password expiry or authentication issue")