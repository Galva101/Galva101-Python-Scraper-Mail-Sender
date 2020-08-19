from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

franceUrl = "https://www.ecdc.europa.eu/en/cases-2019-ncov-eueea"
news = ""

FranceR = requests.get(franceUrl)
FranceSoup = BeautifulSoup(FranceR.text, "html.parser")

data = []
table = FranceSoup.find('table', attrs={})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text for ele in cols]
    data.append([ele for ele in cols]) 

for line in data:
    if( line[0] in ["France", "Italy", "Germany"] ):        
        france = 'Country:\t {} \nSum of Cases:\t {} \nSum of Deaths:\t {} \n14-day cumulative number of COVID-19 cases per 100 000:\t{}\n\n'.format(line[0], line[1], line[2], line[3])
        if( float(line[3]) >60):
            france += "QUARANTINE NECESSARY"
        else:
            france += "No Quarantine Necessary"
        news = news + france + "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n"    

news += "\n\n\n"        

url = "https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/empfehlungen-fuer-reisende/quarantaene-einreisende.html"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
results = soup.find_all("div", attrs={"class": "mod mod-accordion"})

try:
    for result in results:
        try:
            #print(result.get_text().strip())
            news += result.get_text().strip() + "\n"
        except:
            print("error while appending "+result)
except:
    news += "parsing error"
    
news = news.replace("\n\n\n\n", "\n\n")

if( ("Brasilien" or "frankreich" or "frank" or "Frank" )in news):
    news = "FRANKREICH IST IN LISTE GENANNT!!!\n\n\n" + news
print(news)        
        

user = ""  # Enter the Email address that will send the text
name = "ScraPi" # Enter the name that will be displayed in the recipient's inbox
password = ""  # Enter your Email pasword
to = ["", ]  # Enter the Recipients
subject = "Einreiseliste"

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
    #server.sendmail(user, to, msg.as_string())
    server.close()
    print("email sent")
except:
    print("error while sending")

