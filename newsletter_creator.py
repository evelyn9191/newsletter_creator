import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email_data # TODO: Will this usage work?

def check_articles():
    """Parse web for html tag.
    Find class post-thumbnail used for article thumbnails.
    :return: div including links to articles
    """
    url = "https://tyinternety.cz/"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 "
                             "Safari/537.36"}
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all(class_="post-thumbnail")   # How can I make the upper link generate only
                                                    # the a href links within the class
                                                    # and only within the a href, i.e. not include the img tag?
    return articles

def create_email(check_articles, email_data):
    """Send email with links to articles.
    Put class with articles into email as HTML language and send it.
    :param str check_articles
    :return: email with str check_articles
    """
    fromaddr = sender
    toaddr = receiver
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Nova zprava z tyinternety.cz"

    body = articles
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, openkeyword)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Send mail success")

if __name__ == "__main__":
    articles_list = check_articles()
    email = create_email(check_articles, email_data)