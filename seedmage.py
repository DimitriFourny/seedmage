#!/usr/bin/env python3

import random
from datetime import datetime
import sys
import signal
import requests
import os
import torrent
import json
import traceback
from pprint import pprint
import utils
import pickle


def print_info(text):
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  print("\033[33m" + current_time + ": " + text + "\033[0m")


def print_success(text):
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  print("\033[32m" + current_time + ": " + text + "\033[0m")


def print_error(text):
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  print("\033[31m" + current_time + ": " + text + "\033[0m")


def signal_handler(sig, frame):
  print_error("\nClosing SeedMage right now!")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


class Torrent:
  
  def __init__(self, filepath, announce_interval, upload_speed):
    self.seed_per_second = upload_speed * 1024
    self.torrent_file = torrent.File(filepath)
    self.seeder = torrent.Seeder(self.torrent_file)
    self.announce_interval = announce_interval
    self.next_update = self.announce_interval

    self.total_uploaded = 0
    self.total_downloaded = -1
    self.session_uploaded = 0
    self.session_downloaded = 0
    self.threshold = 999999999999999999999
    self.small_torrent_limit = 53687091200                               

    self.name =  "torrent"
    self.firstrun = True
    self.filepath = filepath

    while True:
      print_info("Requesting seeder information")
      try:
        self.seeder.load_peers()
        print_success("done")
        break
      except requests.exceptions.Timeout:
        print_error("timeout")

    self.print_details()

  def load_progress(self):
    progress_file = self.filepath + ".progress"
    file = open(progress_file, "r")
    raw_json = file.read()
    progress = json.loads(raw_json)
    self.total_uploaded = int(progress['total_uploaded'])
    self.total_downloaded = int(progress['total_downloaded'])

  def save_progress(self):
    progress_file = self.filepath + ".progress"

    data = {
      'total_uploaded': str(self.total_uploaded),
      'total_downloaded': str(self.total_downloaded)
    }

    file = open(progress_file, "w")
    file.write(json.dumps(data))
    file.close()

  def update_seed_speed(self):
    seed_speed_file = "seed_speed_file"
    if os.path.isfile(seed_speed_file):
      file = open(seed_speed_file, "r")
      speed = int(file.read())
      self.seed_per_second = speed * 1024

  def print_details(self):
    print_info("Torrent info: " + self.name)
    print(self.torrent_file)

  def print_seeder_info(self):
    print_info("Seeder info: " + self.name)
    print(self.seeder)

  def diff_run(self, interval_diff):
    if self.next_update > 0:
      print_info("Seeder:                " + self.name + " next update: " + str(self.next_update))
      self.next_update = self.next_update - interval_diff
      if self.next_update < interval_diff:
        self.next_update = self.announce_interval
      else:
        return False
    
    self.next_update = self.announce_interval

    if self.seeder.torrent.total_size > self.small_torrent_limit:
      if self.total_downloaded < self.threshold:
        uploaded_bytes = 0      
      else:      
        uploaded_bytes = self.seed_per_second * self.announce_interval
        uploaded_bytes = int(uploaded_bytes * random.uniform(0.45, 0.93)) # +- 20%
        self.total_uploaded += uploaded_bytes
        self.session_uploaded += uploaded_bytes

      diff = int(self.seed_per_second * self.announce_interval * random.uniform(0.9, 1.73))
      self.total_downloaded += diff
      if self.total_downloaded > self.seeder.torrent.total_size:
        self.total_downloaded = self.seeder.torrent.total_size
        self.session_downloaded += 0
      else:
        self.session_downloaded += diff 
    else:
      self.session_uploaded += 0
      self.total_uploaded += 0
      self.session_downloaded += 0
      self.total_downloaded += 0

    return True  

  def first_run(self):
    print_info("First run:             " + self.filepath)
    self.next_update = self.announce_interval

    progress_file = self.filepath + ".progress"
    if os.path.isfile(progress_file):
      print_info("Loaded progress:       " + self.filepath)
      self.load_progress()
    else:
      self.total_uploaded = 0 
      self.total_downloaded = -1 

  def announce(self):
    try:
      self.seeder.upload(self.session_uploaded, self.session_downloaded)      
      self.name = self.seeder.torrent.name     
      print_success("Updated:               " + self.name + " updated") 
      print_info("Threshold:             " + self.name + " size: " + utils.humanbytes(self.threshold))
      print_info("Small Torrent:         " + self.name + " size: " + utils.humanbytes(self.small_torrent_limit))
      print_info("Download info:         " + self.name + " size: " + utils.humanbytes(self.total_downloaded))
      print_info("Upload info:           " + self.name + " size: " + utils.humanbytes(self.total_uploaded))
      print_info("Session Download info: " + self.name + " size: " + utils.humanbytes(self.session_downloaded))
      print_info("Session Upload info:   " + self.name + " size: " + utils.humanbytes(self.session_uploaded))
      print_info("Total size:            " + self.name + " size: " + utils.humanbytes(self.seeder.torrent.total_size))
    except requests.exceptions.Timeout:
      print_error(self.name + " failed to update")
      print("-"*60)
      traceback.print_exc(file=sys.stdout)
      if hasattr(self.seeder.torrent, 'info'):
        pprint(self.seeder.torrent.info)
      print("-"*60)
      utils.sleep(60)

  def seed(self, interval_diff):

    if self.firstrun:
      self.first_run()
    else:
      if self.diff_run(interval_diff) is False:  
        return 

    self.announce()
    self.save_progress()
    self.update_seed_speed()

    self.threshold = self.seeder.torrent.total_size * random.uniform(0.11, 0.22)

    if self.firstrun:
      self.firstrun = False


class Manager:

  directory = "./torrents"
  torrents = []
  toload = []
  known_files = []
  announce_interval = 1800

  def __init__(self):
    self.directory = "./torrents"
    self.torrents = []
    self.toload = []
    self.known_files = []
    self.announce_interval = 1800

  def load(self):
    utils.sleep(10)
    counter = 0

    for filename in list(self.toload):
      kilobytes_per_second = random.uniform(200, 400)
      torrent_file = os.path.join(self.directory, filename)  
      print_info("Torrent: " + torrent_file)
      self.torrents.append(Torrent(torrent_file, self.announce_interval, kilobytes_per_second))
      utils.sleep(2)
      self.toload.remove(filename)     
      counter += 1
      if counter > 24:
        utils.sleep(5)
        return

    utils.sleep(10)

  def remove_old(self):
    try:
      for instance in self.torrents:
        ctime = os.path.getctime(os.path.dirname(os.path.abspath(__file__)) + "/" + instance.filepath)
        if ctime < datetime.datetime.now().timestamp() - (21 * 86400):
          if instance.seeder.torrent.total_size < 107374182400:
            print_info("Removed torrent: " + instance.name)
            self.torrents.remove(instance) 
            os.remove(os.path.dirname(os.path.abspath(__file__)) + "/" + instance.filepath)
            os.remove(os.path.dirname(os.path.abspath(__file__)) + "/" + instance.filepath + ".progress")
    except:
      return 

  def detect_files(self):
    for filename in os.listdir(self.directory):
      if filename.endswith(".torrent"):
        if filename not in self.known_files:
          self.toload.append(filename)
          self.known_files.append(filename)

  def dump_state(self):
    torrents_state_file = "state/torrents_state"
    with open(torrents_state_file, 'wb') as fp:
      pickle.dump(self.torrents, fp, pickle.HIGHEST_PROTOCOL)

    toload_state_file = "state/toload_state"
    with open(toload_state_file, 'wb') as fp:
      pickle.dump(self.toload, fp, pickle.HIGHEST_PROTOCOL)

    known_files_state_file = "state/known_files_state"
    with open(known_files_state_file, 'wb') as fp:
      pickle.dump(self.known_files, fp, pickle.HIGHEST_PROTOCOL)

  def load_state(self):
    torrents_state_file = "state/torrents_state"
    if os.path.exists(torrents_state_file):
      with open(torrents_state_file, 'rb') as fp:
        self.torrents = pickle.load(fp)

    toload_state_file = "state/toload_state"
    if os.path.exists(toload_state_file):
      with open(toload_state_file, 'rb') as fp:
        self.toload = pickle.load(fp)

    known_files_state_file = "state/known_files_state"
    if os.path.exists(known_files_state_file):
      with open(known_files_state_file, 'rb') as fp:
        self.known_files = pickle.load(fp)

  def main(self):
    self.load_state()
    self.detect_files()

    print("Total to load:" + str(len(self.toload)))
    print("")
    self.load()

    while True:
      seeded = 0  
      for instance in self.torrents:
        instance.seed(len(self.torrents))
        utils.sleep(0.75)
        seeded +=1
        if seeded > 24 and len(self.toload) > 0:
          self.load()
          print_success("Loaded: " + str(len(self.torrents)) + ", remaining: " + str(len(self.toload)) + "\n")  
          seeded = 0
        self.dump_state()
        if seeded % 100 == 0:
          print("Seeded:                " + str(seeded) + "/" + str(len(self.torrents)))
      self.remove_old()
      self.detect_files()
      self.dump_state()


if __name__ == "__main__":
  manager = Manager()
  manager.main()
