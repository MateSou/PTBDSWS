import requests
import os

def send_email(to,subject,newUser): 
        email_from = os.getenv('API_FROM')
        email_text = "Novo usuário cadastrado.\n" + "Nome: " + str(newUser) + "\n" + "\nAluno: " + str(os.getenv('NOME')) + "\nPRONTUARIO: " + str(os.getenv('PRONTUARIO'))
        return requests.post(
            os.getenv('API_URL'),
            auth=("api", os.getenv('API_KEY')),
            data={"from": email_from,
                  "to":to,
                "subject":str(os.getenv('FLASK_MAIL_SUBJECT_PREFIX')) + ' - '+ subject,
                "text":email_text})