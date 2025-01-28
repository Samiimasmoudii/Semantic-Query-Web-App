import os
from SPARQLWrapper import SPARQLWrapper, JSON

def execute_sparql_query(query):
    endpoint_url = "https://dbpedia.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    
    try:
        # Add required prefixes if missing
        if "PREFIX dbo:" not in query:
            query = "PREFIX dbo: <http://dbpedia.org/ontology/>\n" + query
        if "PREFIX dbr:" not in query:
            query = "PREFIX dbr: <http://dbpedia.org/resource/>\n" + query

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        
        # Set timeout and user agent
        sparql.setTimeout(30)
        sparql.addCustomParameter("User-Agent", "YourApp/1.0 (your@email.com)")
        
        results = sparql.query().convert()
        return results["results"]["bindings"]
        
    except Exception as e:
        return {"error": f"SPARQL Execution Error: {str(e)}"}

def save_query(query):
    file_path = os.path.join(os.path.dirname(__file__), '../static/sparql_queries.txt')
    with open(file_path, 'a') as f:
        f.write(query + '\n')
