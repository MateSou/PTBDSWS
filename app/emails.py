import requests
import os
def send_email(to,subject,template): 
        email_from = os.getenv('API_FROM')
       # email_text = "\nAluno: " + str(os.getenv('NOME')) + "\nPRONTUARIO: " + str(os.getenv('PRONTUARIO'))
        return requests.post(
            os.getenv('API_URL'),
            auth=("api", os.getenv('API_KEY')),
            data={"from": email_from,
                  "to":to,
                "subject":str(os.getenv('FLASK_MAIL_SUBJECT_PREFIX')) + ' - '+ subject,
                "html":template})
