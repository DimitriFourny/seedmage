# SeedMage
## Usage

```
            .
           /:\
          /;:.\
         //;:. \     SEEDMAGE
        ///;:.. \
  __--"////;:... \"--__
--__   "--_____--"   __--
    """--_______--"""

usage: seedmage.py [-h] [--update-interval UPDATE_INTERVAL]
                   torrent_file upload_speed

positional arguments:
  torrent_file          example.torrent
  upload_speed          Upload speed in kB/s

optional arguments:
  -h, --help            show this help message and exit
  --update-interval UPDATE_INTERVAL
                        Upload interval in seconds
```


## Example

```
$ python seedmage.py "ubuntu.torrent" 1024 --update-interval 10

            .
           /:\
          /;:.\
         //;:. \     SEEDMAGE
        ///;:.. \
  __--"////;:... \"--__
--__   "--_____--"   __--
    """--_______--"""

Torrent:
Announce: https://torrent.ubuntu.com/announce
Date: 2019/10/17 16:38:54
Piece len: 1.0MB
Pieces: 2350
Name: ubuntu-19.10-desktop-amd64.iso
Length: 2.3GB

Seeder:
Peer ID: -DE13F0-yv4SBRaHIQYI
Key: pY32bHY2m4k9
Port: 47956
Update tracker interval: 1800s


Starting seeding at 1.0MB/s
Waiting 10 seconds...
Uploading 11.0MB
Uploaded
```