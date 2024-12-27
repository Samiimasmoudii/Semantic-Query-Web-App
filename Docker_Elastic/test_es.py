import requests
import time

def test_elasticsearch():
    """Test connection to Elasticsearch"""
    url = "http://localhost:9200"
    max_retries = 30
    retry_interval = 1  # seconds

    print(f"Testing connection to Elasticsearch at {url}")
    
    for i in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Successfully connected to Elasticsearch!")
                print("Cluster info:", response.json())
                return True
        except requests.exceptions.ConnectionError:
            print(f"Attempt {i+1}/{max_retries}: Connection failed, retrying in {retry_interval} second...")
            time.sleep(retry_interval)
    
    print("Failed to connect to Elasticsearch after maximum retries")
    return False

if __name__ == "__main__":
    test_elasticsearch()
