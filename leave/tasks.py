import calendar
import datetime as dt
from datetime import datetime, timedelta
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta

today = datetime.now()



def send_email():
    
    send_mail(
           "This method shall work ",
             " A leave request has been made",
            "foneexpress@gmail.com",
            ["yakubtalib70@gmail.com"],
            fail_silently=False,
          )

 
 
 

def start_schedule():

 scheduler = BackgroundScheduler()
 scheduler.add_job(send_email, "interval", minutes=2)

 print("hy")
 scheduler.start()