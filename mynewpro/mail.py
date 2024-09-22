import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = 'h8702643@gmail.com'
        msg['To'] = 'v.gugan16@gmail.com'

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('h8702643@gmail.com', 'osxa rglp zcir cimn')  # Use app password here
            server.sendmail('h8702643@gmail.com', 'v.gugan16@gmail.com', msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

send_email('v.gugan16@gmail.com', 'Hello', 'Hi there!')
