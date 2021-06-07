# SeedMage++

This is a heavily modifed version of seedmage.
https://github.com/DimitriFourny/seedmage

Reasons, why you want to use this version:

* Allows you to seed unlimited torrents
* Also adds download statistics
* Adds download thresholds
* Stops downloading when downloading is complete
* Download and upspeed are with a random threshold to make it look like your speed is going up and down.
* You will never seed faster than you are downloading.
* You will never seed before you have download a certain amount of the file.  How can you seed something you don't have?
* Most large torrents have freeleech so you can set a limit for files that will be downloaded, small torrents will just appears to be seeding.  but are just sitting there to avoid Hit 'n Runs


```
15:37:36: Seeder:                Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL next update: 1800
15:37:37: Updated:               Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL updated
15:37:37: Threshold:             Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL size: 117.11 MB
15:37:37: Small Torrent:         Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL size: 50.00 GB
15:37:37: Download info:         Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL size: 672.83 MB
15:37:37: Upload info:           Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL size: 984.76 MB
15:37:37: Session Download info: Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL size: 0.0 Byte
15:37:37: Session Upload info:   Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL size: 0.0 Byte
15:37:37: Total size:            Thunderbirds.Are.Go.S03E17.1080p.HDTV.H264-DEADPOOL size: 672.83 MB
```
## Usage
### Set the speed
```
# kilobytes per second per torrent
# 10 torrents 10 * 585
# make sure you can do that in a speed test
echo 585 > seed_speed_file
```

### Get your torrents ready
```
mkdir torrents # (should already exist)
cp *.torrent torrents/
```

### Start her up
```
python seedmage.py
```

## Non configurable options
You'll have to configure these in the code if you want to change

### Ignore small torrents
Small torrents are typically seeded by hundreds or thousands of clients. \
It's going to look fairly suspicious if you are seeding it like a lunactic. \
Big torrents tend to seed better (>50GB), also can be freeleech. \
We don't seed torrents < 50GB 
```
self.small_torrent_limit = 53687091200 
```
### Upload threshold
You can't seed something that you haven't partially downloaded. \
If you are wondering, why isn't this seeding? \
Well this means for a 100GB torrents you need to downlaods 11GB to 22GB first before uploading will start. \
So choose freeleech torrents!!!!!! 
```
self.threshold = self.seeder.torrent.total_size * random.uniform(0.11, 0.22)
```   
### Upload speed
```
int(self.seed_per_second * self.announce_interval * random.uniform(0.45, 0.93))
```
### Download
```
int(self.seed_per_second * self.announce_interval * random.uniform(0.9, 1.73))
```
### Announce Interval
```
announce_interval = 1800
```