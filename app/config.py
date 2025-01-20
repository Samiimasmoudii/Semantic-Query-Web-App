import os
import pymysql
pymysql.install_as_MySQLdb()

class Config:
        SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')  # Retrieve SECRET_KEY from environment or use default
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI','mysql://root:newpassword@localhost:5433/users')  # Fixed DB URI for MySQL
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    
# Elasticsearch configurations
es_host = "http://localhost:9200"
es_port = 9200
es_index = "search_logs"
es_doc_type = "logs"
