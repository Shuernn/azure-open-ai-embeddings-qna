from redis import Redis

# Connect to the Redis server
redis_conn = Redis(host="aidna-redis.southeastasia.azurecontainer.io", port=int('6379'), password='redis')
index_name = "embeddings-index"
prompt_index_name = "prompt-index"

# results = redis_conn.ft(index_name).search(query, params_dict)


# Example operations
# redis_client.set("key", "value")  # Set a key-value pair
print(redis_conn.ft("embeddings").delete_document("doc:embeddings:4a494c37714fc41f42525015f1fce4c32a08740a"))
#value = redis_conn.get("doc:embeddings:150e421c5f1971c6f95606666fa562f0ee31e7fd")  # Get the value for a key
#print(value)  # Output: b'value'

# Perform other operations as needed, such as adding documents (embeddings) or performing similarity searches

# Close the Redis connection
redis_conn.close()
