import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


class EmailNotificationSender:
    """
    Implementation of notification sender that sends emails.
    
    Responsibilities:
    - Send email notifications
    - Format email messages
    - Connect to SMTP server
    """
    
    def __init__(
        self, 
        smtp_server: Optional[str] = None, 
        smtp_port: Optional[int] = None,
        username: Optional[str] = None, 
        password: Optional[str] = None,
        from_email: Optional[str] = None
    ):
        """
        Initialize the email sender
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            username: SMTP username
            password: SMTP password
            from_email: Sender email address
        """
        self.smtp_server = smtp_server or "smtp.example.com"
        self.smtp_port = smtp_port or 587
        self.username = username or "banking_notifications@example.com"
        self.password = password or "password"  # In a real app, use secure storage
        self.from_email = from_email or "banking_notifications@example.com"
        self.logger = logging.getLogger(__name__)
    
    def send_email(self, recipient: str, subject: str, body: str) -> None:
        """
        Send an email notification
        
        Args:
            recipient: Email recipient
            subject: Email subject
            body: Email body
        """
        # In a real application, you would use smtplib to send an actual email
        # For this example, we'll just log it
        self.logger.info(f"Sending email to {recipient}")
        self.logger.info(f"Subject: {subject}")
        self.logger.info(f"Body: {body}")
        
        # Uncomment this code to actually send emails in a production environment
        """
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.from_email
            message["To"] = recipient
            message["Subject"] = subject
            
            # Add body
            message.attach(MIMEText(body, "plain"))
            
            # Connect to server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.username, self.password)
                server.send_message(message)
                
            self.logger.info(f"Email sent successfully to {recipient}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipient}: {str(e)}")
        """
    
    def send_sms(self, phone_number: str, message: str) -> None:
        """
        Send an SMS notification
        
        Args:
            phone_number: Recipient phone number
            message: SMS message
        """
        # In a real application, you would use a service like Twilio to send an SMS
        # For this example, we'll just log it
        self.logger.info(f"Sending SMS to {phone_number}")
        self.logger.info(f"Message: {message}")
        
        # Uncomment and adapt this code to use a real SMS service in production
        """
        try:
            # Example using Twilio (you would need to install the twilio package)
            from twilio.rest import Client
            
            account_sid = 'your_account_sid'
            auth_token = 'your_auth_token'
            client = Client(account_sid, auth_token)
            
            message = client.messages.create(
                body=message,
                from_='+1234567890',  # Your Twilio number
                to=phone_number
            )
            
            self.logger.info(f"SMS sent successfully to {phone_number}")
            
        except Exception as e:
            self.logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
        """
