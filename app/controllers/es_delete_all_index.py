from elasticsearch import Elasticsearch
import traceback

from es_config import es_client  # Import your Elasticsearch client configuration

try:
    # Check connection
    if not es_client.ping():
        raise ValueError("Elasticsearch connection failed!")

    # Get all indexes
    indexes = es_client.indices.get_alias(index="*").keys()  # Use index="*" as a keyword argument

    if indexes:
        # Loop through each index and delete it
        for index in indexes:
            es_client.indices.delete(index=index)
            print(f"Deleted index: {index}")
        print("All indexes have been deleted.")
    else:
        print("No indexes found to delete.")
except Exception as err:
    print(f"Error: {err}\n{traceback.format_exc()}")
