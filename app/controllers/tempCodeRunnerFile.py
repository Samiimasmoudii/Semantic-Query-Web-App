from elasticsearch import Elasticsearch
from elasticsearch import helpers as es_helpers
import traceback
import json

from es_config import es_host, es_port, es_index, es_doc_type,es_client,es_bulk_index_flag


# Paths for Files
sparql_queries_path = "app/static/sparql_queries.txt"  # File containing SPARQL queries
es_mapping_path = "app/static/es_mapping.json"
try:
    # Push Index Mapping to Elasticsearch
    with open(es_mapping_path, "r") as mapping_file:
        mapping_data = mapping_file.read()
        mapping_document = json.loads(mapping_data)
        if not es_client.indices.exists(index=es_index):
            es_client.indices.create(index=es_index, body=mapping_document)
            print(f"Created index: {es_index}")
        else:
            print(f"Index already exists: {es_index}")

    # Reading SPARQL Queries
    with open(sparql_queries_path, "r", encoding="utf-8") as queries_file:
        queries = queries_file.read().split("\n\n")  # Assuming queries are separated by double newline

    actions = []

    # Preparing Bulk Actions
    for idx, query in enumerate(queries, start=1):
        if query.strip():  # Only process non-empty queries
            actions.append({
                "_index": es_index,
                "_id": str(idx),
                "_source": {"query": query.strip()}
            })

        if len(actions) == es_bulk_index_flag:
            es_helpers.bulk(es_client, actions)
            print(f"Pushed batch of {es_bulk_index_flag} queries")
            actions = []

    # Push Remaining Queries
    if actions:
        es_helpers.bulk(es_client, actions)
        print(f"Pushed remaining {len(actions)} queries")

    # Print total documents indexed
    print(f"Total documents indexed: {es_client.count(index=es_index)['count']}")

except Exception as err:
    print(f"Error: {err}\n{traceback.format_exc()}")