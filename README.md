# COSC 381 class project README

## Requirements

To make sure you have the required software installed, run the following command in the command prompt:
python3 -m pip install -r requirements.txt


## Config file
Initialize the variables api_key and ce_id as strings copy-pasted from your configuration/setup webpages. 

## cse.py
Initialize my_search_topic on line 8 with desired search term. Running the script will send the first 100 results to a json file.

## download_youtube_data.py
Takes search term (preferably a video id) as system argument when the script is called in the command line i.e.
$ python3 download_youtube_data.py ['video_id']
The result will be output to a json file specified on line 21


## download_youtube_data_batch.sh
Calls download_youtube_data.py on every line of a specified file (line 6). The resulting json files are added to a folder, youtube_data

## create_data_for_indexing.py
creates the file data_for_indexing.json which contains the video_id, title, description of all the videos in youtube_data (see last heading)

## create_whoosh_index.py
Creates a whoosh index from the data file created by create_data_for_indexing.py