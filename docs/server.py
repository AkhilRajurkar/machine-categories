from flask import Flask, jsonify, send_from_directory
import os
import json
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__, static_url_path='')

# MongoDB connection
client = MongoClient('mongodb+srv://rajurkarakhil:category123@category.hit1a.mongodb.net/?retryWrites=true&w=majority&appName=category')
db = client['machinery_db']
english_collection = db['ss_schemas']
german_collection = db['ss_schemas_de']

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

@app.route('/')
def root():
    return send_from_directory('.', 'index.html')

@app.route('/api/categories/<language>')
def get_categories(language):
    try:
        # Load the appropriate language file
        filename = f'categories_{language}.json'
        data = load_json_file(filename)
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Categories not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/schema/<language>/<code>')
def get_schema(language, code):
    try:
        # Select collection based on language
        collection = english_collection if language == 'en' else german_collection
        
        # Find the schema in MongoDB using the exact code
        schema = collection.find_one({
            "$or": [
                {"sub_subcategory_code": code},
                {"unterunterkategorie_code": code}
            ]
        })
        
        if schema:
            # Convert MongoDB document to JSON and remove internal fields
            schema_json = json.loads(json_util.dumps(schema))
            if '_id' in schema_json:
                del schema_json['_id']
            
            # Add SEO tags if not present
            if 'seo_tags' not in schema_json:
                schema_json['seo_tags'] = [
                    schema_json.get('category', ''),
                    schema_json.get('subcategory', ''),
                    schema_json.get('sub_subcategory', ''),
                    schema_json.get('sub_subcategory_code', '')
                ]
            
            # Add manufacturer information if not present
            if 'manufacturer_info' not in schema_json:
                schema_json['manufacturer_info'] = {
                    'european': False,  # Default value
                    'certifications': []  # Default empty list
                }
            
            # Add debug information
            print(f"Found schema for code {code}: {schema_json}")
            return jsonify(schema_json)
        else:
            print(f"No schema found for code {code} in {language} collection")
            return jsonify({'error': 'Schema not found'}), 404
    except Exception as e:
        print(f"Error fetching schema: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 