#!/usr/local/bin/python

import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import sys

sys.path.insert(0, '../InstaPy/')

from instapy import InstaPy

insta_username = os.environ.get('INSTA_USER')
insta_password = os.environ.get('INSTA_PASSWORD')
email_username = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASSWORD')

def main():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = 'hashtags.csv'

    with open('{}/{}'.format(dir_path, file_name), 'r+') as f:
        reader = csv.reader(f)
        tags = [row[0] for row in reader]

    session = InstaPy(username=insta_username, password=insta_password,
                      headless_browser=True, multi_logs=False)
    try:
        session.login()

        number_of_likes_by_tag = int(900 / len(tags))
        session.set_upper_follower_count(limit=3000)
        session.like_by_tags(tags, amount=number_of_likes_by_tag)
        
        if session.liked_img < 900:
                number_of_likes_by_tag = int((900 - session.liked_img) / len(tags))
                session.like_by_tags(tags, amount=number_of_likes_by_tag)
    
        body = 'Number of images liked: {}'.format(session.liked_img)
        _send_report(body=body)

    except Exception as exception:
        _send_report(subject='Something when wrong on Instagramer', body=str(exception))

    finally:
        session.end()


def _send_report(**kwargs):
    
    toaddr = "roger.domenech.aguilera@gmail.com, demayorquierosermochilera@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = toaddr
    msg['Subject'] = kwargs.get('subject', 'Instagramer report')
     
    body = kwargs.get('body', '')
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.live.com', 587)
    server.starttls()
    server.login(email_username, email_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


if __name__ == ('__main__'):
    main()
