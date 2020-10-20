#!/usr/bin/python

import sys
import pprint
from googleapiclient.discovery import build
import json

my_api_key = 'AIzaSyAP0Z7Emwtlc9-CdmLtjhzsmZrE51Sig-o'
my_cse_id = '85a32bc71eb8779f0'
video_id = sys.argv[1]

#print(video_id)

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey = api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

if __name__ == '__main__':
   results = google_search(video_id, my_api_key, my_cse_id, num =1) 
   out_file = open("./youtube_data/" + video_id + ".json", "w")
   json.dump(results, out_file, indent = 6)
   out_file.close()
   #pprint.pprint(results)
