import os
from SPARQLWrapper import SPARQLWrapper, JSON

def execute_sparql_query(query):
    endpoint_url = "https://dbpedia.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        return {"error": str(e)}

def save_query(query):
    file_path = os.path.join(os.path.dirname(__file__), '../static/sparql_queries.txt')
    with open(file_path, 'a') as f:
        f.write(query + '\n')
