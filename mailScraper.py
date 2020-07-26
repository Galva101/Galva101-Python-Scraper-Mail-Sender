from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

r = requests.get("https://www.spieletipps.de/news/1/")
soup = BeautifulSoup(r.text, "html.parser")
headlines = soup.find_all("h2", attrs={"class": "component-headline teaser-headline"})
a = soup.find_all('a', href=True) #finding all "href" links for the articles

links = []
for a in a:
    links.append(a['href']) ##append all link endings for the url into a new list
links = links[12:] #remove all leading and trailing links not related to articles
links = links[:-12]

i = 1
news = ""

for new in headlines:
    news += ("%s - \t " % i)
    new = new.text.strip()
    new = new.replace("\n", " ")
    news += new 
    try:
        news += " https://www.spieletipps.de{}".format(links[i-1])
    except:
        print("formatting error at "+new+" ignoring...")
    news += "\n"
    if (i%5==0):
        news += "\n"
    i += 1

user = ""  # Enter the Email address that will send the text
name = "ScraPy" # Enter the name that will be displayed in the recipient's inbox
password = ""  # Enter your Email pasword
to = ["", ]  # Enter the Recipients
subject = "Spieletipps Summary"

msg = MIMEMultipart("alternative")
msg.set_charset("utf-8")

msg["Subject"] = subject
msg["From"] = "{} <{}>".format(name, user)
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

