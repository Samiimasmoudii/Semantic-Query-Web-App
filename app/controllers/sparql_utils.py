import os
from SPARQLWrapper import SPARQLWrapper, JSON
import requests

from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.parse import quote_plus
import requests

def execute_sparql_query(query):
    try:
        print("Executing SPARQL Query:", query)  # Debugging
        response = requests.get(
            "https://dbpedia.org/sparql",
            params={"query": query, "format": "json"},
            timeout=5
        )
        response.raise_for_status()  # Raise error if request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"SPARQL request failed: {str(e)}")  # Debugging
        return {"error": f"SPARQL request failed: {str(e)}"}


def save_query(query):
    file_path = os.path.join(os.path.dirname(__file__), '../static/sparql_queries.txt')
    with open(file_path, 'a') as f:
        f.write(query + '\n')
