'''
Fake torrent seeder
'''

import argparse
import random
import time

import torrent
import utils


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

torrent_file = torrent.File(args.torrent_file)
print("Torrent:")
print(torrent_file)

seeder = torrent.Seeder(torrent_file)
seeder.load_peers()
print("Seeder:")
print(seeder)

seed_per_second = args.upload_speed * 1024
update_interval = seeder.update_interval
if args.update_interval: 
  # override the update_interval given by the server
  update_interval = args.update_interval 

print("\nStarting seeding at %s/s" % utils.sizeof_fmt(seed_per_second))
total_uploaded = 0
while True:
  print("Waiting %d seconds..." % update_interval)
  time.sleep(update_interval)
 
  uploaded_bytes = seed_per_second * update_interval
  uploaded_bytes = int(uploaded_bytes * random.uniform(0.8, 1.2)) # +- 20%
  print("Uploading %s" % utils.sizeof_fmt(uploaded_bytes))

  total_uploaded += uploaded_bytes
  seeder.upload(total_uploaded)
  print("Uploaded")