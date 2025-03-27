from pymongo import MongoClient
import json
from bson import json_util

def check_mongo_connection():
    try:
        # MongoDB connection
        client = MongoClient('mongodb+srv://rajurkarakhil:category123@category.hit1a.mongodb.net/?retryWrites=true&w=majority&appName=category')
        db = client['machinery_db']
        
        # Check English collection
        en_collection = db['ss_schemas']
        en_count = en_collection.count_documents({})
        print(f"\nEnglish schemas count: {en_count}")
        if en_count > 0:
            print("\nSample English schema:")
            sample_en = en_collection.find_one({})
            print(json.dumps(json.loads(json_util.dumps(sample_en)), indent=2))
        
        # Check German collection
        de_collection = db['ss_schemas_de']
        de_count = de_collection.count_documents({})
        print(f"\nGerman schemas count: {de_count}")
        if de_count > 0:
            print("\nSample German schema:")
            sample_de = de_collection.find_one({})
            print(json.dumps(json.loads(json_util.dumps(sample_de)), indent=2))
        
        # Print all unique category codes
        print("\nUnique category codes in English collection:")
        en_codes = en_collection.distinct('category_code')
        print(en_codes)
        
        print("\nUnique category codes in German collection:")
        de_codes = de_collection.distinct('category_code')
        print(de_codes)
        
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking MongoDB connection and data...")
    check_mongo_connection() 