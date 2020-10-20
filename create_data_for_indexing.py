from pathlib import Path
import json
import pprint

paths = [str(x) for x in Path('./youtube_data').glob('**/*.json')]
results = []
for path in paths:
    with open(path, 'r') as f:
        data = json.load(f)

        video =  {
            'id': path[15:24],
            'title': data[0]['title'],
            'description':  data[0]['snippet']
        }
        results.append(video)


with open('data_for_indexing.json', 'w') as dump_file:
    json.dump(results, dump_file)
