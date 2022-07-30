import smtplib
from email.message import EmailMessage
import datetime as dt

from app.db.database import SessionLocal
from app.models.models import User


def check_for_last_quiz_date_passed():
    db = SessionLocal()
    now = dt.datetime.now()
    delta = dt.timedelta(hours=168)
    time_delta = now - delta
    users = db.query(User).filter(str(User.last_quiz_done_date) < str(time_delta)).all()
    comp_email = "a.kostenkouk@gmail.com"
    comp_pass = "uqguamyzqkjpduab"
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(comp_email, comp_pass)
        for user_info in users:
            msg = EmailMessage()
            msg['subject'] = str(user_info.last_quiz_done)
            msg['to'] = str(user_info.email)
            msg['from'] = comp_email
            msg.set_content(f'PLease pass the Quiz: {user_info.last_quiz_done} again.\n'
                            f'Your last date passed: {user_info.last_quiz_done_date}.\n'
                            f'Your last score:{user_info.last_quiz_score}.\n'
                            f'Following link: ...')
            smtp.send_message(msg)
        smtp.quit()
    db.close()
    return None


check_for_last_quiz_date_passed()
