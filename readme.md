## Install Python and set up  virtual environment 
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
pip install flask rdflib sparqlwrapper


## Compose docker image 

docker-compose up -d 

to test the connection from your local machine to teh docker image :  curl http://localhost:9200

or 
pip install requests
python test_es.py

If the server is running correctly you can try creating an index and adding some data 
# PowerShell commands (if  you're using Windows)

# Create an index
Invoke-RestMethod -Method PUT -Uri "http://localhost:9200/test_index"

# Add a document
$body = @{
    "title" = "Test Document"
    "content" = "Hello World"
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri "http://localhost:9200/test_index/_doc" -Body $body -ContentType "application/json"
# Retrieve the document you just created:

Invoke-RestMethod -Method GET -Uri "http://localhost:9200/test_index/_doc/sEKwB5QBb6fV7ijn4281"

# Search all documents in the index:


Invoke-RestMethod -Method GET -Uri "http://localhost:9200/test_index/_search" -ContentType "application/json"


# Add another document with specific search terms:


$body = @{
    "title" = "Another Document"
    "content" = "This is searchable content"
    "tags" = @("test", "example")
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri "http://localhost:9200/test_index/_doc" -Body $body -ContentType "application/json"

# Perform a search query:
$searchBody = @{
    "query" = @{
        "match" = @{
            "content" = "searchable"
        }
    }
} | ConvertTo-Json

Invoke-RestMethod -Method GET -Uri "http://localhost:9200/test_index/_search" -Body $searchBody -ContentType "application/json"

# Get index statistics:
Invoke-RestMethod -Method GET -Uri "http://localhost:9200/test_index/_stats"


# Check how many documents are in the index:

Invoke-RestMethod -Method GET -Uri "http://localhost:9200/test_index/_count"