#!/usr/local/bin/python

import argparse
import schedule
import time

from do_likes import main

max_likes = 950

parser = argparse.ArgumentParser()
parser.add_argument('--likes', type=int, help='Number of likes (less than 1000).')
parser.add_argument('--time', help='UTC time.')

args = parser.parse_args()

if args.likes:
    max_likes = args.likes

if args.time:
    schedule.every().day.at(args.time).do(main, max_likes)
else:
    main(max_likes)

while True:
    schedule.run_pending()
    time.sleep(1)