#!/usr/local/bin/python

import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import smtplib
import sys

sys.path.insert(0, '../InstaPy/')

from instapy import InstaPy

insta_username = os.environ.get('INSTA_USER')
insta_password = os.environ.get('INSTA_PASSWORD')
email_username = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASSWORD')

dir_path = os.path.dirname(os.path.realpath(__file__))

max_likes = 900
max_retries = 40

users_filename = 'users.csv'
tags_filename = 'hashtags.csv'

comments = [
    'Very nice pic @{}, I really love it!',
    'I love this picture @{}!!!',
    'What an amazing photo @{}!!',
    'You have an awesome instagram account! If you want you can check mine...',
    "I've checked your instagram account and it's awesome!"
    ]


def interact(session, tags):

    friends = read_csv('{}/{}'.format(dir_path, users_filename))

    counter = 0
    session.set_relationship_bounds(
        enabled=True, potency_ratio=None,
        delimit_by_numbers=True, max_followers=3000,
        max_following=100000, min_followers=50, min_following=100)
    session.set_dont_include(friends)
    #session.set_do_comment(enabled=True, percentage=25)
    #session.set_comments(comments, media='Photo')

    for tag in tags:
        number_of_likes_by_tag = round((max_likes - session.liked_img) / (len(tags) - counter))
        session.like_by_tags([tag], amount=number_of_likes_by_tag)
        counter += 1


def read_csv(path):
    with open(path, 'r+') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]


def main():

    retries_count = 0

    tags = read_csv('{}/{}'.format(dir_path, tags_filename))

    session = InstaPy(username=insta_username, password=insta_password, headless_browser=True,
                      multi_logs=False, nogui=True)

    session.login()
    
    while retries_count < max_retries:
        try:
            likes_by_tag = round((max_likes - session.liked_img) / len(tags))
            if likes_by_tag == 0:
                pending_likes = round((max_likes - session.liked_img) % len(tags))
                tag = random.choice(tags)
                session.like_by_tags([tag], amount=pending_likes)
                break

            interact(session, tags)

        except Exception as exception:
            print(exception)
            retries_count += 1
            # _send_report(subject='Something when wrong on Instagramer', body=str(exception))

    session.end()


def _send_report(**kwargs):
    
    toaddr = "roger.domenech.aguilera@gmail.com, demayorquierosermochilera@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = toaddr
    msg['Subject'] = kwargs.get('subject', 'Instagramer report')
     
    body = kwargs.get('body', '')
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_username, email_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


if __name__ == ('__main__'):
    main()
