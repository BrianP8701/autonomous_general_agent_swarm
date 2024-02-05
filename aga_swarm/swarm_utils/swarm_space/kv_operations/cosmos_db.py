'''
A single container is used for all operations for all users.

CosmosDB automatically splits the container into physical partitions and does all the scaling.
We just need to choose 3 logical partitions and have an id field for retrieval.

The swarm object will hold 2 of the partiton keys and the keys to get the swarm container.

Partition keys: user_id/swarm_id/category
"category" can be "action_space_metadata", "util_space_metadata", "memory_space_metadata", "swarm_state" etc.

The "id" field will be the key for the document.
"id" might be like "action_id", "util_id", "memory_id", "node_id" etc.

In this manner we have good logical partitions and can provide a standard interface for all KV operations.
'''

from azure.cosmos import CosmosClient, PartitionKey
from typing import Any

from aga_swarm.swarm.types import Swarm

def upload_swarm_space_kv_document(swarm: Swarm, category: str, key: str, document: dict):
    url = swarm.configs.azure_cosmos_db_url
    cosmos_key = swarm.configs.azure_cosmos_db_key
    container_name = swarm.configs.azure_cosmos_db_container_name
    client = CosmosClient(url, credential=cosmos_key)
    database_name = client.get_database_client(swarm.configs.azure_cosmos_db_database_name)
    container = database_name.get_container_client(container_name)
    
    # Add partiton keys and id field. CosmosDB expects all values to be inside the dict.
    document['id'] = key
    document['category'] = category
    document['user_id'] = swarm.user_id
    document['swarm_id'] = swarm.swarm_id
    
    try:
        container.upsert_item(document)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

def retrieve_swarm_space_kv_document(swarm: Swarm, category: str, key: str):
    url = swarm.configs.azure_cosmos_db_url
    cosmos_key = swarm.configs.azure_cosmos_db_key
    container_name = swarm.configs.azure_cosmos_db_container_name
    client = CosmosClient(url, credential=cosmos_key)
    database_name = client.get_database_client(swarm.configs.azure_cosmos_db_database_name)
    container = database_name.get_container_client(container_name)
    partition_key = f'{swarm.user_id}/{swarm.swarm_id}/{category}'
    partition_key = PartitionKey(partition_key)
    
    try:
        document = container.read_item(item=key, partition_key=key)
        return {'success': True, 'error_message': '', 'data': document}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

def delete_swarm_space_kv_document(swarm: Swarm, category: str, key: str):
    url = swarm.configs.azure_cosmos_db_url
    cosmos_key = swarm.configs.azure_cosmos_db_key
    container_name = swarm.configs.azure_cosmos_db_container_name
    client = CosmosClient(url, credential=cosmos_key)
    database_name = client.get_database_client(swarm.configs.azure_cosmos_db_database_name)
    container = database_name.get_container_client(container_name)
    partition_key = f'{swarm.user_id}/{swarm.swarm_id}/{category}'
    partition_key = PartitionKey(partition_key)
    
    try:
        container.delete_item(item=key, partition_key=key)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
