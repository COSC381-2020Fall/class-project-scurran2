import json
import sys
from googleapiclient.discovery import build
import config

my_api_key = config.api_key
def youtube_data(video_id):
    service = build("youtube", "v3", developerKey=my_api_key)
    result = service.videos().list(part='snippet', id=video_id).execute()
    return result

if __name__ == '__main__':
    video_id = sys.argv[1]
    result = youtube_data(video_id)
    with open('youtube_data/' + video_id + '.json', 'w') as f:
        json.dump(result, f, indent=6)