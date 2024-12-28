# Elasticsearch configurations
from elasticsearch import Elasticsearch


es_host = "http://localhost:9200"
es_port = 9200
es_index = "search_logs"
es_doc_type = "logs"
es_client = Elasticsearch(
    "http://localhost:9200"
) 
es_bulk_index_flag = 1000