#! /usr/bin/bash
mkdir youtube_data
while read line;
do
	 python3 download_youtube_data.py $line 
done <video_ids.txt

