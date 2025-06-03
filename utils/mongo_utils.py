# utils/mongo_utils.py
import pymongo
import os
import streamlit as st # Using streamlit for caching connection

@st.cache_resource # Cache the client connection
def init_connection():
    """Initializes a connection to MongoDB Atlas using credentials from environment variables."""
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        st.error("MONGO_URI not found in environment variables. Please check your .env file.")
        return None
    try:
        client = pymongo.MongoClient(mongo_uri)
        # The ismaster command is cheap and does not require auth.
        client.admin.command("ismaster")
        print("MongoDB connection successful.")
        return client
    except pymongo.errors.ConfigurationError as ce:
        st.error(f"MongoDB Configuration Error: {ce}. Check connection string format.")
        print(f"MongoDB Configuration Error: {ce}")
        return None
    except pymongo.errors.ConnectionFailure as cf:
        st.error(f"MongoDB Connection Failure: {cf}. Check URI, credentials, network access, and IP allowlist in Atlas.")
        print(f"MongoDB Connection Failure: {cf}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred connecting to MongoDB: {e}")
        print(f"An unexpected error occurred connecting to MongoDB: {e}")
        return None

def get_database():
    """Gets the MongoDB database object."""
    client = init_connection()
    if client:
        db_name = os.getenv("MONGO_DB_NAME")
        if not db_name:
            st.error("MONGO_DB_NAME not found in environment variables. Please check your .env file.")
            return None
        try:
            db = client[db_name]
            # Optional: Check if DB exists by listing collections (can be slow)
            # collection_names = db.list_collection_names()
            # print(f"Connected to database 	{db_name}	. Collections: {collection_names}")
            print(f"Connected to database: {db_name}")
            return db
        except Exception as e:
            st.error(f"Error accessing database 	{db_name}	: {e}")
            print(f"Error accessing database 	{db_name}	: {e}")
            return None
    return None

# Example usage (optional, for testing):
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # Load .env for local testing
    db = get_database()
    if db:
        print(f"Successfully got database object for: {db.name}")
        print("Available collections:")
        try:
            for name in db.list_collection_names():
                print(f"- {name}")
        except Exception as e:
            print(f"Could not list collections: {e}")
    else:
        print("Failed to get database object.")

