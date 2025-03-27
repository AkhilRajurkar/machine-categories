from flask import Flask, jsonify, send_from_directory
import os
import json
import logging
from datetime import datetime
from pymongo import MongoClient
from bson import json_util

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='')

# MongoDB connection
try:
    client = MongoClient('mongodb+srv://rajurkarakhil:category123@category.hit1a.mongodb.net/?retryWrites=true&w=majority&appName=category')
    db = client['machinery_db']
    english_collection = db['ss_schemas']
    german_collection = db['ss_schemas_de']
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise

def load_json_file(file_path):
    try:
        logger.debug(f"Attempting to load JSON file: {file_path}")
        if not os.path.exists(file_path):
            logger.warning(f"File does not exist: {file_path}")
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.debug(f"Successfully loaded JSON file: {file_path}")
            return data
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return None

def get_schema_from_static_file(language, code):
    """Get schema from static JSON file for GitHub Pages."""
    try:
        logger.info(f"Attempting to get schema from static file for language: {language}, code: {code}")
        
        # Remove any leading zeros from the code
        code = code.lstrip('0')
        logger.debug(f"Code after stripping leading zeros: {code}")
        
        # Handle different code formats (e.g., "1.15.12" vs "1.15.12")
        if '.' in code:
            parts = code.split('.')
            if len(parts) == 3:
                # Format: X.YY.ZZ
                code = f"{parts[0]}.{parts[1]}.{parts[2]}"
            elif len(parts) == 2:
                # Format: X.YY
                code = f"{parts[0]}.{parts[1]}"
            logger.debug(f"Formatted code: {code}")
        
        # Define base paths for schema files
        base_paths = [
            os.path.join('docs', f'schemas_{language}'),
            os.path.join('.', 'docs', f'schemas_{language}'),
            f'schemas_{language}',  # Fallback to old path
        ]
        
        # Try each base path
        for base_path in base_paths:
            # Try different file name formats
            file_formats = [
                f'{code}.json',
                f'{code.zfill(2)}.json',
                f'{code.replace(".", "_")}.json'
            ]
            
            for file_format in file_formats:
                full_path = os.path.join(base_path, file_format)
                logger.debug(f"Trying path: {full_path}")
                
                if os.path.exists(full_path):
                    logger.info(f"Found schema file at: {full_path}")
                    schema = load_json_file(full_path)
                    if schema:
                        logger.info(f"Successfully loaded schema for code {code}")
                        return schema
                    else:
                        logger.warning(f"Schema file exists but could not be loaded: {full_path}")
        
        logger.warning(f"No schema found for code: {code} in any location")
        return None
        
    except Exception as e:
        logger.error(f"Error in get_schema_from_static_file: {e}", exc_info=True)
        return None

@app.route('/')
def root():
    return send_from_directory('docs', 'index.html')

@app.route('/api/categories/<language>')
def get_categories(language):
    try:
        logger.info(f"Getting categories for language: {language}")
        # Load from docs directory
        filename = os.path.join('docs', f'categories_{language}.json')
        data = load_json_file(filename)
        if data:
            logger.info(f"Successfully retrieved categories for {language}")
            return jsonify(data)
        else:
            logger.warning(f"Categories not found for language: {language}")
            return jsonify({'error': 'Categories not found'}), 404
    except Exception as e:
        logger.error(f"Error getting categories: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/schema/<language>/<code>')
def get_schema(language, code):
    try:
        logger.info(f"Requesting schema for language: {language}, code: {code}")
        
        # First try to get schema from static file (for GitHub Pages)
        schema = get_schema_from_static_file(language, code)
        
        if not schema:
            logger.info(f"Schema not found in static files, trying MongoDB...")
            # If not found in static files, try MongoDB
            collection = english_collection if language == 'en' else german_collection
            logger.debug(f"Using collection: {collection.name}")
            
            # Try different query patterns
            query_patterns = [
                {"sub_subcategory_code": code},
                {"unterunterkategorie_code": code},
                {"sub_subcategory_code": code.lstrip('0')},
                {"unterunterkategorie_code": code.lstrip('0')},
                {"sub_subcategory_code": code.replace('.', '')},
                {"unterunterkategorie_code": code.replace('.', '')}
            ]
            
            for query in query_patterns:
                logger.debug(f"Trying MongoDB query: {query}")
                schema = collection.find_one(query)
                if schema:
                    logger.info(f"Found schema in MongoDB using query: {query}")
                    schema = json.loads(json_util.dumps(schema))
                    if '_id' in schema:
                        del schema['_id']
                    break
            
            if not schema:
                logger.warning(f"No schema found for code {code} in {language} collection")
                return jsonify({'error': 'Schema not found'}), 404
        
        # Add SEO tags if not present
        if 'seo_tags' not in schema:
            schema['seo_tags'] = [
                schema.get('category', ''),
                schema.get('subcategory', ''),
                schema.get('sub_subcategory', ''),
                schema.get('sub_subcategory_code', '')
            ]
            logger.debug("Added SEO tags to schema")
        
        # Add manufacturer information if not present
        if 'manufacturer_info' not in schema:
            schema['manufacturer_info'] = {
                'european': False,  # Default value
                'certifications': []  # Default empty list
            }
            logger.debug("Added manufacturer information to schema")
        
        logger.info(f"Successfully returning schema for code {code}")
        return jsonify(schema)
        
    except Exception as e:
        logger.error(f"Error fetching schema: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 