# Newsletter creator takes tags containing links to articles
# from homepage tyinternety.cz and sends the tags as html text
# within an email to receiver's email address. Script is then
# run on personal computer once a week via Windows Task Scheduler.
#
# There has to be module :email_data with email account access info.
# The module has to include variables:
# * openkeyword: password for gmail account
# * sender: sender email address
# * receiver: receiver email address

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email_data


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
    articles = soup.find_all(class_="entry-title")

    return articles


def create_email(check_articles, email_data):
    """Send email with links to articles.

    Put class with articles into email as HTML language and send it.

    :param [str] check_articles: List with extracted article titles and links.
    :param module email_data: Module with variables with email access info.
    """
    fromaddr = email_data.sender
    toaddr = email_data.receiver
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Nove clanky z tyinternety.cz"

    articles = "\n ".join(check_articles)
    body = "Toto jsou nejnovejsi clanky z tyinternety.cz:\n {}".format(articles)
    msg.attach(MIMEText(body, "plain", "utf-8"))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, email_data.openkeyword)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Send mail success")


if __name__ == "__main__":
    articles_list = check_articles()
    send_email = create_email(check_articles=articles_list, email_data=email_data)
