# Selery - bu Pythonda yozilgan ochiq manbali taqsimlangan vazifalar navbati tizimi.
# U bir nechta ishchi jarayonlar yoki mashinalar bo'ylab vazifalarni ko'pincha ko'p vaqt
# talab qiladigan yoki resurs talab qiladigan boshqarish va taqsimlashda yordam berish uchun mo'ljallangan.



from celery import Celery

def send_email(email_name:str):

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "ibodullofayzullayev2001@gmail.com"
    receiver_email = email_name
    password = "yyawsnczbigqxmad"

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a>

           <button>  <a href="http://t.me/Ibodullo_Fayzullayev01">My Telegram</a> </button>
           has many great tutorials.
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

emails = ["dilshodbekdosmurodov45@gmail.com" , "ibodullofayzullayev2001@gmail.com" ]

app = Celery('send_message', broker='amqp://guest@localhost//')

@app.task
def send_message():
    for i in emails:
        send_email(i)


