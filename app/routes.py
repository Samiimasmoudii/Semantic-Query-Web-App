from flask import Blueprint, render_template, request, jsonify
from .sparql_utils import execute_sparql_query

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
