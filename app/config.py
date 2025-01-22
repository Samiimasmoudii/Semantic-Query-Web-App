import os
import pymysql
from dotenv import load_dotenv
from datetime import timedelta
# Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

# Load environment variables from the .env file
load_dotenv()

class Config:
    """
    Configuration class for Flask application settings.
    Retrieves all configurations from the environment variables.
    """
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Database connection URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Disable SQLAlchemy event tracking to improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')
    permanent_session_lifetime = timedelta(minutes=30)



# Optional: Elasticsearch configurations (only fetched from environment variables)
es_host = os.getenv('ES_HOST')
es_port = int(os.getenv('ES_PORT', 9200))  # Default to 9200 if not provided
es_index = os.getenv('ES_INDEX', 'search_logs')  # Default to 'search_logs'
es_doc_type = os.getenv('ES_DOC_TYPE', 'logs')  # Default to 'logs'
