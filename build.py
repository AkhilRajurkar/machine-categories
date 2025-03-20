import os
import json

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"Warning: File is empty: {file_path}")
                return None
            try:
                return json.loads(content)
            except json.JSONDecodeError as je:
                print(f"JSON parsing error in {file_path}:")
                print(f"Error details: {str(je)}")
                return None
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None

def get_numeric_code(code):
    # Convert code to numeric value for sorting (e.g., "2" -> 2, "02" -> 2)
    try:
        return int(str(code).split('.')[0])
    except:
        return 999  # Default high number for invalid codes

def build_categories_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths for both languages
    paths = {
        'en': os.path.join(script_dir, "category_new", "english"),
        'de': os.path.join(script_dir, "category_new", "german")
    }
    
    # Define output files for both languages
    outputs = {
        'en': os.path.join(script_dir, "categories_en.json"),
        'de': os.path.join(script_dir, "categories_de.json")
    }
    
    for lang, base_path in paths.items():
        print(f"\nProcessing {lang.upper()} categories...")
        
        category_map = {}
        processed_files = []
        failed_files = []
        
        if os.path.exists(base_path):
            for file in os.listdir(base_path):
                if file.endswith(f'_{lang}.json'):
                    file_path = os.path.join(base_path, file)
                    print(f"Processing: {file}")
                    data = load_json_file(file_path)
                    if data:
                        numeric_code = get_numeric_code(data['code'])
                        category_map[numeric_code] = data
                        processed_files.append(f"{numeric_code:02d} - {data['name']}")
                    else:
                        failed_files.append(file)
        
        # Sort categories by numeric code
        sorted_codes = sorted(category_map.keys())
        categories = [category_map[code] for code in sorted_codes]
        
        # Write combined categories to JSON file
        with open(outputs[lang], 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)
        
        print(f"\nProcessed {lang.upper()} Categories:")
        for item in sorted(processed_files):
            print(f"- {item}")
        
        if failed_files:
            print(f"\nFailed to process ({lang}):")
            for file in failed_files:
                print(f"- {file}")
        
        print(f"\nTotal {lang.upper()} categories: {len(categories)}")
        print(f"Output written to: {outputs[lang]}")

if __name__ == "__main__":
    build_categories_json() 