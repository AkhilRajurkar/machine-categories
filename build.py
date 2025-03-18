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
        categories = []
        processed_files = []
        failed_files = []
        
        print(f"\nProcessing {lang.upper()} categories:")
        
        # Load all category files for current language
        if os.path.exists(base_path):
            for file in os.listdir(base_path):
                if file.endswith(f'_{lang}.json'):
                    file_path = os.path.join(base_path, file)
                    print(f"\nProcessing: {file}")
                    data = load_json_file(file_path)
                    if data:
                        categories.append(data)
                        processed_files.append(file)
                    else:
                        failed_files.append(file)
        
        # Write combined categories to language-specific JSON file
        with open(outputs[lang], 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)
        
        print(f"\nSummary for {lang.upper()}:")
        print(f"Successfully processed ({len(processed_files)}): {', '.join(processed_files)}")
        print(f"Failed to process ({len(failed_files)}): {', '.join(failed_files)}")
        print(f"Created {outputs[lang]} with {len(categories)} categories")

if __name__ == "__main__":
    build_categories_json() 