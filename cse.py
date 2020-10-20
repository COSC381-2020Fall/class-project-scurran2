import pprint
from googleapiclient.discovery import build
import json
import config

my_api_key = config.api_key
my_cse_id = config.cse_id
my_search_topic = 'Karpov' #phrase to search in 365 chess

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey = api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

if __name__ == '__main__':
    results = []
    for i in range (0,91,10):
         results.append(google_search(my_search_topic, my_api_key, my_cse_id, num=10, start=i))
    out_file = open("google_search.json", "w")
    json.dump(results, out_file, indent = 6)
    out_file.close()
  # pprint.pprint(results)
