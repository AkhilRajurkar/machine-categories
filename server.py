from flask import Flask, jsonify, send_from_directory
import os
import json

app = Flask(__name__, static_url_path='')

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

@app.route('/')
def root():
    return send_from_directory('.', 'index.html')

@app.route('/api/categories')
def get_categories():
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "category_new", "english")
    
    categories = []
    
    # Load all English category files
    if os.path.exists(base_path):
        for file in os.listdir(base_path):
            if file.endswith('_en.json'):
                file_path = os.path.join(base_path, file)
                data = load_json_file(file_path)
                if data:
                    categories.append(data)
    
    return jsonify(categories)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 