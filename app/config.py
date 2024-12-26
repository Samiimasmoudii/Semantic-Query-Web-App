import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
# Elasticsearch configurations
es_host = "https://localhost:9200"
es_port = 9200
es_index = "search_logs"
es_doc_type = "logs"