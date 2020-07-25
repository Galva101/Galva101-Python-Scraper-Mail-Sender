from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

i = 1
news = ""
r = requests.get("https://www.spieletipps.de/news/1/")
soup = BeautifulSoup(r.text, "html.parser")
result = soup.find_all("h2", attrs={"class": "component-headline teaser-headline"})

for new in result:
    new = new.text.strip()
    new = new.replace("\n", " ")
    new = new.replace("\t", "")
    if not len(new)<=15: #Minimum Headline Length
        news += ("%s - \t " % i)
        news += new
        news += "\n"
        i += 1

#news = news.replace("ö", "oe")
#news = news.replace("ä", "ae")
#news = news.replace("ü", "ue")
#news = news.replace("ß", "ss")
#news = news.replace("é", "e")
#news = news.replace("è", "e")

user = ""  # Enter your Email address
password = ""  # Enter your Email pasword
to = recipients = ["", ]  # Enter the Recipients
subject = "News Summary"

msg = MIMEMultipart("alternative")
msg.set_charset("utf-8")

msg["Subject"] = subject
msg["From"] = user
msg["To"] = ", ".join(to)

msg.attach(MIMEText(news, "plain"))#the message is attached here

try:
    server = smtplib.SMTP_SSL("mail.gmx.net", 465) #preset for GMX mail accounts
    server.ehlo()
    server.login(user, password)
    server.sendmail(user, to, msg.as_string())
    server.close()
    print("email sent")
except:
    print("error while sending")
