import pymongo
import json
import os

# Connection string provided by the user
MONGO_URI = "mongodb+srv://Admin:Admin@cluster0.nazx3vn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
JSON_FILE_PATH = "/home/ubuntu/upload/fecomdb.json"
DATABASE_NAME = "fecomdb_data" # You can change this if needed

def import_data_to_mongodb():
    """Connects to MongoDB Atlas, reads data from a JSON file, 
       and inserts it into the specified database and collection.
    """
    try:
        # Load data from JSON file
        print(f"Attempting to load JSON from: {JSON_FILE_PATH}")
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("JSON file loaded successfully.")

        # Debug: Print the keys found at the top level
        found_keys = list(data.keys())
        print(f"Found top-level keys: {found_keys}")

        # Check if there is exactly one top-level key
        if len(found_keys) != 1:
            print(f"Error: Expected exactly one top-level key (collection name), but found {len(found_keys)}: {found_keys}")
            return

        collection_name = found_keys[0]
        documents_to_insert = data[collection_name]

        if not isinstance(documents_to_insert, list):
            print(f"Error: The value associated with key '{collection_name}' is not a list of documents.")
            return

        print(f"Using collection name: {collection_name}")
        print(f"Number of documents to insert: {len(documents_to_insert)}")

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

        # Select database and collection
        db = client[DATABASE_NAME]
        collection = db[collection_name]

        # Optional: Clear existing data in the collection before inserting new data
        print(f"Clearing existing documents in collection '{collection_name}'...")
        collection.delete_many({})
        print(f"Existing documents cleared (if any).")

        # Insert data
        print(f"Inserting {len(documents_to_insert)} documents into collection '{collection_name}' in database '{DATABASE_NAME}'...")
        result = collection.insert_many(documents_to_insert)
        print(f"Successfully inserted {len(result.inserted_ids)} documents.")

    except FileNotFoundError:
        print(f"Error: JSON file not found at {JSON_FILE_PATH}")
    except json.JSONDecodeError as jde:
        print(f"Error: Could not decode JSON from file {JSON_FILE_PATH}. Details: {jde}")
    except pymongo.errors.ConfigurationError as ce:
        print(f"MongoDB Configuration Error: {ce}. Please check your connection string and network access.")
    except pymongo.errors.ConnectionFailure as cf:
         print(f"MongoDB Connection Failure: {cf}. Could not connect to the server. Check URI, credentials, and network.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    import_data_to_mongodb()

