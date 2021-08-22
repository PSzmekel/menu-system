import datetime
import threading
import time
from models import Dish
import json

class mailing(threading.Thread):
    def __init__(self, value):
        threading.Thread.__init__(self)
        self.value = value
    def run(self):
        while True:
            # Removing the date and microseconds from the full format
            t = str(datetime.datetime.now())[11:-7]

            if t == '10:00:00':
                sender = 'from@fromdomain.com'
                receivers = ['to@todomain.com']

                message = json.dumps(Dish.listForMail())

                try:
                    smtpObj = smtplib.SMTP('localhost')
                    smtpObj.sendmail(sender, receivers, message)
                except SMTPException:
                    print('Error: unable to send email')

                time.sleep(1)
