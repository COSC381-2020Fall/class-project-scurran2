from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.lang.porter import stem
import sys
import json

ix = open_dir("indexdir")


def query(query_str, items_per_page=10, current_page=1):
    query_str = stem(query_str)	
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("description", ix.schema).parse(query_str)	        
        results = searcher.search(query, limit=None)
        num_query_results = len(results)
        query_results = []
        start = (current_page-1)*items_per_page
        end = start + items_per_page
        for i in range(start, min(len(results), end)):
            d={}
            d['url'] = "https://www.youtube.com/watch?v=%s" % results[i]['id']
            d['title'] = results[i]['title']
            d['description'] = results[i].highlights('description')
            d['score'] = results[i].score    
            query_results.append(d)	            


        return query_results, num_query_results	        


if __name__ == "__main__":
    query_str = sys.argv[1]
    items_per_page = int(sys.argv[2])
    current_page = int(sys.argv[3])
    query_results = query(query_str, items_per_page, current_page)
    print(json.dumps(query_results)) 