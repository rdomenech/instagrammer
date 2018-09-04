#!/usr/local/bin/python

import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import smtplib
import sys
import schedule
import time

sys.path.insert(0, '../InstaPy/')

from instapy import InstaPy

insta_username = os.environ.get('INSTA_USER')
insta_password = os.environ.get('INSTA_PASSWORD')
email_username = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASSWORD')

dir_path = os.path.dirname(os.path.realpath(__file__))

max_retries = 40

users_filename = 'users.csv'
tags_filename = 'hashtags.csv'

def interact(session, tags, max_likes):

    friends = read_csv('{}/{}'.format(dir_path, users_filename))

    counter = 0
    session.set_relationship_bounds(
        enabled=True, potency_ratio=None,
        delimit_by_numbers=True, max_followers=3000,
        max_following=100000, min_followers=50, min_following=100)
    session.set_dont_include(friends)

    for tag in tags:
        number_of_likes_by_tag = round((max_likes - session.liked_img) / (len(tags) - counter))
        session.like_by_tags([tag], amount=number_of_likes_by_tag)
        counter += 1


def read_csv(path):
    with open(path, 'r+') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]

def main(max_likes):

    print('Running intagramer with max_likes = {}'.format(max_likes))

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

            interact(session, tags, max_likes)

        except Exception as exception:
            print(exception)
            retries_count += 1

    session.end()

if __name__ == ('__main__'):
    main()
