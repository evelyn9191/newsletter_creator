# Newsletter creator extracts article titles and their urls
# from homepage tyinternety.cz and sends those by email.
#
# There has to be module :email_data with email account access info.
# The module has to include variables:
# * openkeyword: password for gmail account
# * sender: sender email address
# * receiver: receiver email address
from typing import List, Tuple

import requests

from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_data import sender, receiver, openkeyword


def get_article_pairs() -> List[Tuple[str, str]]:
    """Parse web tyinternety.cz and find articles and their titles."""
    url = "https://tyinternety.cz/"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 "
                             "Safari/537.36"}
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all(class_="entry-title")
    article_soup = BeautifulSoup(str(articles), 'lxml')

    cleaned_articles_data = []
    for article_data in article_soup.find_all("a"):
        cleaned_articles_data.append((article_data.string, article_data["href"]))

    return cleaned_articles_data


def send_email(article_pairs: List[Tuple[str, str]], fromaddr: str, toaddr: str, openkeyword: str):
    """Send email with article titles and their urls."""
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = toaddr
    msg['Subject'] = 'Nové články na tyinternety.cz'
    body = MIMEText(('\n\n'.join('{}\n{}'.format(title, url) for (title, url) in article_pairs)), 'plain')
    msg.attach(body)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, openkeyword)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Email successfully sent!")


if __name__ == "__main__":
    article_pairs = get_article_pairs()
    send_email(article_pairs, sender, receiver, openkeyword)
