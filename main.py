from json_to_word_converter import JsonToWordConverter
import os
import json

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                print(f"Warning: Empty file {file_path}")
                return None
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def get_category_files():
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "category_new")
    
    categories = {
        'english': {},
        'german': {}
    }
    
    # Load English files
    en_path = os.path.join(base_path, "english")
    if os.path.exists(en_path):
        for file in os.listdir(en_path):
            if file.endswith('.json'):
                file_path = os.path.join(en_path, file)
                category_name = file.replace('_en.json', '')
                data = load_json_file(file_path)
                if data:
                    categories['english'][category_name] = data
                    print(f"Loaded English category: {category_name}")
    
    # Load German files
    de_path = os.path.join(base_path, "german")
    if os.path.exists(de_path):
        for file in os.listdir(de_path):
            if file.endswith('.json'):
                file_path = os.path.join(de_path, file)
                category_name = file.replace('_de.json', '')
                data = load_json_file(file_path)
                if data:
                    categories['german'][category_name] = data
                    print(f"Loaded German category: {category_name}")
    
    # Add validation for loaded categories
    for lang in ['english', 'german']:
        for category_name in list(categories[lang].keys()):
            if not categories[lang][category_name]:
                print(f"Removing invalid {lang} category: {category_name}")
                del categories[lang][category_name]
    
    return categories

def main():
    try:
        # Initialize converter
        converter = JsonToWordConverter()
        
        # Get all category files
        print("Loading category files...")
        categories = get_category_files()
        
        if not categories['english'] and not categories['german']:
            print("No category files were loaded. Please check if the files exist in the correct locations.")
            return
        
        # Define output paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_docx_en = os.path.join(script_dir, "categories_en.docx")
        output_docx_de = os.path.join(script_dir, "categories_de.docx")
        
        # Convert English categories to Word
        if categories['english']:
            en_data = {
                "categories": [cat_data for cat_data in categories['english'].values() if cat_data]
            }
            converter.convert(en_data, output_docx_en)
            print(f"Created English document: {output_docx_en}")
        
        # Convert German categories to Word
        if categories['german']:
            de_data = {
                "categories": [cat_data for cat_data in categories['german'].values() if cat_data]
            }
            converter.convert(de_data, output_docx_de)
            print(f"Created German document: {output_docx_de}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
