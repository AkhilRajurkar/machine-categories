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

def get_schema_from_static_file(language, code):
    """Get schema from static JSON file for GitHub Pages."""
    try:
        # Remove any leading zeros from the code
        code = code.lstrip('0')
        
        # Handle different code formats (e.g., "1.15.12" vs "1.15.12")
        if '.' in code:
            parts = code.split('.')
            if len(parts) == 3:
                # Format: X.YY.ZZ
                code = f"{parts[0]}.{parts[1]}.{parts[2]}"
            elif len(parts) == 2:
                # Format: X.YY
                code = f"{parts[0]}.{parts[1]}"
        
        schema_dir = f'docs/schemas_{language}'
        schema_file = f'{code}.json'
        schema_path = os.path.join(schema_dir, schema_file)
        
        print(f"Looking for schema at: {schema_path}")
        if os.path.exists(schema_path):
            schema = load_json_file(schema_path)
            if schema:
                print(f"Found schema for code {code}")
                return schema
            else:
                print(f"Schema file exists but is empty or invalid: {schema_path}")
        else:
            print(f"No schema file found at {schema_path}")
            # Try alternative code formats
            alt_codes = [
                f"{code}.json",
                f"{code.zfill(2)}.json",
                f"{code.replace('.', '_')}.json"
            ]
            for alt_code in alt_codes:
                alt_path = os.path.join(schema_dir, alt_code)
                if os.path.exists(alt_path):
                    schema = load_json_file(alt_path)
                    if schema:
                        print(f"Found schema using alternative code: {alt_code}")
                        return schema
        return None
    except Exception as e:
        print(f"Error loading static schema: {e}")
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
        print(f"Requesting schema for language: {language}, code: {code}")
        
        # First try to get schema from static file (for GitHub Pages)
        schema = get_schema_from_static_file(language, code)
        
        if not schema:
            # If not found in static files, try MongoDB
            collection = english_collection if language == 'en' else german_collection
            schema = collection.find_one({
                "$or": [
                    {"sub_subcategory_code": code},
                    {"unterunterkategorie_code": code}
                ]
            })
            
            if schema:
                schema = json.loads(json_util.dumps(schema))
                if '_id' in schema:
                    del schema['_id']
                print(f"Found schema in MongoDB for code {code}")
            else:
                print(f"No schema found for code {code} in {language} collection")
                return jsonify({'error': 'Schema not found'}), 404
        
        # Add SEO tags if not present
        if 'seo_tags' not in schema:
            schema['seo_tags'] = [
                schema.get('category', ''),
                schema.get('subcategory', ''),
                schema.get('sub_subcategory', ''),
                schema.get('sub_subcategory_code', '')
            ]
        
        # Add manufacturer information if not present
        if 'manufacturer_info' not in schema:
            schema['manufacturer_info'] = {
                'european': False,  # Default value
                'certifications': []  # Default empty list
            }
        
        # Add debug information
        print(f"Returning schema for code {code}")
        return jsonify(schema)
        
    except Exception as e:
        print(f"Error fetching schema: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 