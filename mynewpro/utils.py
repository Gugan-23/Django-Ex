# myapp/utils/mongodb.py

from pymongo import MongoClient

def get_mongo_client():
    username = 'vgugan16'
    password = 'gugan2004'
    uri = f"mongodb+srv://{username}:{password}@cluster0.qyh1fuo.mongodb.net/?retryWrites=true&w=majority"
    
    try:
        client = MongoClient(uri)
        client.admin.command('ping')  # Check connection
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
# utils.py (or wherever you want to place the function)

# utils.py
# utils.py
import smtplib
from email.mime.text import MIMEText
from django.conf import settings

def send_email(to_email, subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = to_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, to_email, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
