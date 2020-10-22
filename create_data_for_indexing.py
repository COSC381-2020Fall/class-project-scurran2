from pathlib import Path
import json
import pprint

paths = [str(x) for x in Path('./youtube_data').glob('**/*.json')]
results = []
for path in paths:
    print(path)
    with open(path, 'r') as f:
        data = json.load(f)
        video_data = data['items'][0]
        video =  {
            'id': video_data['id'],
            'title': video_data['snippet']['title'],
            'description': video_data['snippet']['description']
        }
        results.append(video)


with open('data_for_indexing.json', 'w') as dump_file:
    json.dump(results, dump_file)
