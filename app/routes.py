from flask import Blueprint, render_template, request, jsonify
from app.controllers.es_pull_scroll import es_search
from .controllers.sparql_utils import execute_sparql_query 

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/query', methods=['POST'])
def query():
    query = request.form.get('sparql_query')
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    results = execute_sparql_query(query)
    if "error" in results:
        return jsonify({"error": results["error"]}), 400

    return jsonify({"results": results})
@main.route('/test', methods=['GET'])
def test_pipeline():
    """
    Test the pipeline: query Elasticsearch and use the result to query DBpedia.
    """
    try:
        # Step 1: Query Elasticsearch for a search term
        search_term = request.args.get('query', default='Albert Einstein')
        es_results = es_search(search_term)

        # Step 2: Use SPARQL to query DBpedia with the first Elasticsearch result
        if es_results:
            sparql_query = es_results[0].get("search_term", search_term)
            dbpedia_results = execute_sparql_query(sparql_query)

            return jsonify({
                "elasticsearch_results": es_results,
                "dbpedia_results": dbpedia_results
            })

        return jsonify({"message": "No results found in Elasticsearch."})
    except Exception as e:
        return jsonify({"error": f"Pipeline testing failed: {e}"}), 500