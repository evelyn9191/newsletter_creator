# Newsletter creator extracts tags containing article titles and their urls
# from homepage tyinternety.cz, cleans them from html and sends those
# by email to receiver's email address. Script is then run on personal computer
# once a week via Windows Task Scheduler.
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


def get_articles():
    """Parse web for html tags.

    Find class entry-title used in article titles tags.

    :return: [dict] with article titles as keys and article urls as values
    """
    url = "https://tyinternety.cz/"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 "
                             "Safari/537.36"}
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all(class_="entry-title")
    article_soup = BeautifulSoup(str(articles), 'lxml')
    urls = str(article_soup.find_all('a'))
    urls_list = urls.split('</a>, ')
    articles_dict = {}
    for value in urls_list:
        head, sep, tail = value.partition('\">')
        tag, part, link = head.partition('href=\"')
        if '</a>]' in tail:
            tail = tail.replace('</a>]', '')
        if 'bookmark' in link:
            url, separator, bookmark = link.partition('\"')
            articles_dict[tail] = url
        else:
            articles_dict[tail] = link
    return articles_dict


def create_email(get_articles, email_data):
    """Send email with article titles and their urls.

    Nicely format article titles and urls, attach them to email body and send the email.

    :param [dict] get_articles: Dictionary with extracted article titles and urls.
    :param module email_data: Module with variables with email access info.
    """
    articles_dict = get_articles()
    fromaddr = email_data.sender
    toaddr = email_data.receiver
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Nové články na tyinternety.cz'
    body = MIMEText(('\n\n'.join('{}\n{}'.format(key, value) for key, value in articles_dict.items())), 'plain')
    msg.attach(body)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, email_data.openkeyword)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Email successfully sent!")


if __name__ == "__main__":
    get_articles()
    create_email(get_articles, email_data)
