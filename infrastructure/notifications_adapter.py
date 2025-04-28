# infrastructure/notifications/notification_adapter.py
from abc import ABC, abstractmethod

class NotificationAdapter(ABC):
    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str):
        pass

    @abstractmethod
    def send_sms(self, number: str, message: str):
        pass



# infrastructure/notifications/fake_notification_service.py
class FakeNotificationService(NotificationAdapter):
    def send_email(self, recipient, subject, body):
        print(f"[EMAIL to {recipient}] Subject: {subject} | Body: {body}")

    def send_sms(self, number, message):
        print(f"[SMS to {number}] Message: {message}")
