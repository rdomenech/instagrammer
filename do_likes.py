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


def read_csv(path):
    with open(path, 'r+') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]


def main(max_likes):

    print('Running intagramer with max_likes = {}'.format(max_likes))

    retries_count = 0

    users = ['lamochiladesara', 'juntos_viajando', 'justwotravel', 'viajeroscallejeros', 'traveloveroma', 
             'viviendodeviaje', 'sofiapozuelo', 'el_viajedetuvida']

    friends = read_csv('{}/{}'.format(dir_path, users_filename))
    tags = read_csv('{}/{}'.format(dir_path, tags_filename))
    session = InstaPy(username=insta_username, password=insta_password, headless_browser=True,
                      multi_logs=False, nogui=True)

    session.login()
    
    session.set_simulation(enabled=False)
    #session.set_mandatory_words(tags)
    session.set_user_interact(amount=1, randomize=True, percentage=50, media='Photo')
    session.set_do_like(enabled=True, percentage=50)
    session.set_do_follow(enabled=False, percentage=0)
    session.set_relationship_bounds(
        enabled=True, potency_ratio=None,
        delimit_by_numbers=True, max_followers=3000,
        max_following=10000, min_followers=20, min_following=100)
    session.set_dont_include(friends)

    pending_likes = max_likes - session.liked_img 

    try:
        while pending_likes > 0:
            number_of_likes_by_user = round(pending_likes / len(users))

            if number_of_likes_by_user == 0:
                session.interact_user_followers(['de_mayor_quiero_ser_mochilera'], amount=pending_likes, randomize=True)
                break
        
            session.interact_user_followers(users, amount=number_of_likes_by_user, randomize=True)
            pending_likes = max_likes - session.liked_img 
    except Exception as e:
        print(e)
        session.end()

    session.end()

if __name__ == ('__main__'):
    main()
