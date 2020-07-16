#!/usr/bin/env python3
'''
Fake torrent seeder
'''

import argparse
import random
import time
import sys
import signal
import requests

import torrent
import utils

def print_wip(text):
  print(text + "...", end='', flush=True)


def print_info(text):
  print("\033[33m" + text + "\033[0m")

def print_success(text):
  print("\033[32m" + text + "\033[0m")

def print_error(text):
  print("\033[31m" + text + "\033[0m")

def signal_handler(sig, frame):
    print_error("\nClosing SeedMage right now!")
    sys.exit(0)

print(r'''
            .
           /:\
          /;:.\
         //;:. \     SEEDMAGE
        ///;:.. \
  __--"////;:... \"--__
--__   "--_____--"   __--
    """--_______--"""
''')

parser = argparse.ArgumentParser()
parser.add_argument("torrent_file", help="example.torrent")
parser.add_argument("upload_speed", help="Upload speed in kB/s", type=int)
parser.add_argument("--update-interval", help="Upload interval in seconds", 
    type=int)
args = parser.parse_args()

signal.signal(signal.SIGINT, signal_handler)

# Torrent general information
torrent_file = torrent.File(args.torrent_file)
print_info("Torrent:")
print(torrent_file)

# Requesting seeder information to the tracker
seeder = torrent.Seeder(torrent_file)
while True:
  print_wip("Requesting seeder information")
  try:
    seeder.load_peers()
    print_success("done")
    break
  except requests.exceptions.Timeout:
    print_error("timeout")

print_info("Seeder:")
print(seeder)

# Calculate a few parameters
seed_per_second = args.upload_speed * 1024
update_interval = seeder.update_interval
if args.update_interval: 
  # override the update_interval given by the server
  update_interval = args.update_interval 

# Seeding
print_info("\nStarting seeding at %s/s" % utils.sizeof_fmt(seed_per_second))
total_uploaded = 0
while True:
  print_wip("Waiting %d seconds" % update_interval)
  time.sleep(update_interval)
  print_success("done")

  uploaded_bytes = seed_per_second * update_interval
  uploaded_bytes = int(uploaded_bytes * random.uniform(0.8, 1.2)) # +- 20%
  total_uploaded += uploaded_bytes

  while True:
    print_wip("Uploading %s" % utils.sizeof_fmt(uploaded_bytes))
    try:
      seeder.upload(total_uploaded)
      print_success("uploaded")
      break
    except requests.exceptions.Timeout:
      print_error("timeout")