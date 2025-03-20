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
                print(f"Near text: {content[max(0, je.pos-20):je.pos+20]}")
                return None
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None

def build_categories_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "category_new", "english")
    output_path = os.path.join(script_dir, "categories.json")
    
    categories = []
    processed_files = []
    failed_files = []
    
    # Create a mapping of code to category for proper ordering
    category_map = {}
    
    # Load all English category files
    if os.path.exists(base_path):
        for file in os.listdir(base_path):
            if file.endswith('_en.json'):
                file_path = os.path.join(base_path, file)
                print(f"\nProcessing: {file}")
                data = load_json_file(file_path)
                if data:
                    # Store in map using code as key
                    category_map[data['code']] = data
                    processed_files.append(file)
                else:
                    failed_files.append(file)
    
    # Sort categories by code and create final list
    sorted_codes = sorted(category_map.keys(), key=lambda x: int(str(x).split('.')[0]))
    categories = [category_map[code] for code in sorted_codes]
    
    # Write combined categories to a single JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    
    print(f"\nSummary:")
    print(f"Successfully processed ({len(processed_files)}) files:")
    for code in sorted_codes:
        print(f"{code}: {category_map[code]['name']}")
    print(f"\nFailed to process ({len(failed_files)}): {', '.join(failed_files)}")
    print(f"Created categories.json with {len(categories)} categories")

if __name__ == "__main__":
    build_categories_json() 