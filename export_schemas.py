#!/usr/bin/env python3
"""
Export MongoDB schemas to static JSON files for GitHub Pages hosting.
This script connects to MongoDB, retrieves all schemas from the collections,
and saves them as individual JSON files in the appropriate directories.
"""

import os
import json
from pymongo import MongoClient
from bson import json_util
import argparse

def ensure_dir(directory):
    """Ensure the directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def export_schemas(connection_string, db_name, output_dir):
    """
    Export schemas from MongoDB to static JSON files.
    
    Args:
        connection_string: MongoDB connection string
        db_name: Database name
        output_dir: Base output directory
    """
    # Connect to MongoDB
    client = MongoClient(connection_string)
    db = client[db_name]
    
    # Export English schemas
    en_collection = db['ss_schemas']
    en_dir = os.path.join(output_dir, 'schemas_en')
    ensure_dir(en_dir)
    
    # Export German schemas
    de_collection = db['ss_schemas_de']
    de_dir = os.path.join(output_dir, 'schemas_de')
    ensure_dir(de_dir)
    
    # Export English schemas
    print("Exporting English schemas...")
    for schema in en_collection.find():
        if 'sub_subcategory_code' in schema:
            code = schema['sub_subcategory_code']
            filename = os.path.join(en_dir, f"{code}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_util.dumps(schema, indent=2))
            print(f"  Exported {code} to {filename}")
    
    # Export German schemas
    print("Exporting German schemas...")
    for schema in de_collection.find():
        if 'unterunterkategorie_code' in schema:
            code = schema['unterunterkategorie_code']
            filename = os.path.join(de_dir, f"{code}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_util.dumps(schema, indent=2))
            print(f"  Exported {code} to {filename}")
    
    print("Export completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export MongoDB schemas to static JSON files")
    parser.add_argument("--conn", default="mongodb+srv://rajurkarakhil:category123@category.hit1a.mongodb.net/?retryWrites=true&w=majority&appName=category", 
                        help="MongoDB connection string")
    parser.add_argument("--db", default="machinery_db", help="Database name")
    parser.add_argument("--out", default="./", help="Output directory")
    
    args = parser.parse_args()
    export_schemas(args.conn, args.db, args.out) 