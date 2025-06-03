import pymongo
import json
import os

# Connection string provided by the user
MONGO_URI = "mongodb+srv://Admin:Admin@cluster0.nazx3vn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
JSON_FILE_PATH = "/home/ubuntu/upload/fecomdb.json"
DATABASE_NAME = "fecomdb_data" # Database to store all collections

def import_all_collections_to_mongodb():
    """Connects to MongoDB Atlas, reads data from a JSON file containing multiple collections,
       and inserts each collection into the specified database.
    """
    client = None # Initialize client to None for finally block
    try:
        # Load data from JSON file
        print(f"Attempting to load JSON from: {JSON_FILE_PATH}")
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("JSON file loaded successfully.")

        # Check if the loaded data is a dictionary
        if not isinstance(data, dict):
            print("Error: Expected JSON file to contain a dictionary (object) at the top level.")
            return

        collection_keys = list(data.keys())
        print(f"Found {len(collection_keys)} potential collections (top-level keys): {collection_keys}")

        if not collection_keys:
            print("Error: No collections found in the JSON file.")
            return

        # Connect to MongoDB
        print(f"Connecting to MongoDB Atlas at {MONGO_URI[:30]}...") # Print only prefix for security
        client = pymongo.MongoClient(MONGO_URI)

        # Ping the server to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return

        # Select database
        db = client[DATABASE_NAME]
        print(f"Using database: 	{DATABASE_NAME}")

        total_inserted_count = 0
        # Iterate through each key (collection name) and its data (list of documents)
        for collection_name, documents_to_insert in data.items():
            print(f"\nProcessing collection: 	{collection_name}")

            if not isinstance(documents_to_insert, list):
                print(f"Warning: Skipping key 	'{collection_name}	' because its value is not a list of documents.")
                continue

            if not documents_to_insert:
                print(f"Warning: Skipping collection 	'{collection_name}	' because it has no documents.")
                continue

            print(f"Number of documents found: 	{len(documents_to_insert)}")

            # Select collection
            collection = db[collection_name]

            # Optional: Clear existing data in the collection before inserting new data
            print(f"Clearing existing documents in collection 	'{collection_name}	'...")
            delete_result = collection.delete_many({})
            print(f"Cleared {delete_result.deleted_count} existing documents.")

            # Insert data
            print(f"Inserting {len(documents_to_insert)} documents into collection 	'{collection_name}	'...")
            try:
                result = collection.insert_many(documents_to_insert)
                inserted_count = len(result.inserted_ids)
                total_inserted_count += inserted_count
                print(f"Successfully inserted {inserted_count} documents into 	'{collection_name}	'.")
            except Exception as insert_error:
                print(f"Error inserting documents into collection 	'{collection_name}	': {insert_error}")

        print(f"\nImport process finished. Total documents inserted across all collections: {total_inserted_count}")

    except FileNotFoundError:
        print(f"Error: JSON file not found at {JSON_FILE_PATH}")
    except json.JSONDecodeError as jde:
        print(f"Error: Could not decode JSON from file {JSON_FILE_PATH}. Details: {jde}")
    except pymongo.errors.ConfigurationError as ce:
        print(f"MongoDB Configuration Error: {ce}. Please check your connection string and network access.")
    except pymongo.errors.ConnectionFailure as cf:
         print(f"MongoDB Connection Failure: {cf}. Could not connect to the server. Check URI, credentials, and network.")
    except Exception as e:
        print(f"An unexpected error occurred during the import process: {e}")
    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    import_all_collections_to_mongodb()

