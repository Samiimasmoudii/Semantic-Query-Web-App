from elasticsearch import Elasticsearch
from elasticsearch import helpers as es_helpers
import traceback
import json
from ..config import es_host, es_port, es_index, es_doc_type

# Elasticsearch Client
es_client = Elasticsearch([es_host])

def es_search(keyword):
    """
    Search Elasticsearch for SPARQL queries matching the keyword.
    """
    try:
        request_body = get_request_body(keyword)
        output_dict_list = []

      
        scroller = es_helpers.scan(
            client=es_client,
            index=es_index,
            query=request_body,
            scroll="1m",
            preserve_order=True,
            size=1000,
            request_timeout=60,
            raise_on_error=False
        )

        # Retrieve and store results
        for es_output in scroller:
            score = es_output["_score"]
            source = es_output["_source"]
            source["score"] = score
            output_dict_list.append(source)
        
        return output_dict_list

    except Exception as err:
        print(f"Error: {err}\n{traceback.format_exc()}")

def get_request_body(keyword):
    """
    Create Elasticsearch query for SPARQL matching the keyword.
    """
    if len(keyword) >= 3:
        fuzziness_param = 2
    else:
        fuzziness_param = "AUTO"

    request_body = {
        "query": {
            "match": {
                "query": {
                    "query": keyword,
                    "fuzziness": fuzziness_param,
                    "prefix_length": 0
                }
            }
        }
    }
    return request_body
