import os
import json

def clean_code(code):
    """Remove leading zeros from code parts while preserving structure"""
    if not code:
        return code
    parts = str(code).split('.')
    cleaned_parts = [str(int(part)) for part in parts]
    return '.'.join(cleaned_parts)

def update_json_file(file_path):
    try:
        # First verify if file exists and has content
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return False
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"Empty file: {file_path}")
                return False
            data = json.loads(content)
            
        # Clean main category code
        data['code'] = clean_code(data['code'])
        
        # Clean subcategory codes
        for subcat in data.get('subcategories', []):
            subcat['code'] = clean_code(subcat['code'])
            # Clean sub-subcategory codes
            for subsubcat in subcat.get('subSubcategories', []):
                subsubcat['code'] = clean_code(subsubcat['code'])
        
        # Write back the cleaned data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully updated: {file_path}")
        return True
        
    except json.JSONDecodeError as je:
        print(f"Invalid JSON in {file_path}: {je}")
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def update_all_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    problematic_files = []
    successful_files = []
    
    # Update both English and German files
    for lang in ['english', 'german']:
        base_path = os.path.join(script_dir, "category_new", lang)
        if os.path.exists(base_path):
            print(f"\nProcessing {lang.upper()} files...")
            for file in os.listdir(base_path):
                if file.endswith('.json'):
                    file_path = os.path.join(base_path, file)
                    if update_json_file(file_path):
                        successful_files.append(file)
                    else:
                        problematic_files.append(file)
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Successfully processed {len(successful_files)} files")
    if problematic_files:
        print(f"\nProblematic files that need attention ({len(problematic_files)}):")
        for file in problematic_files:
            print(f"- {file}")

if __name__ == "__main__":
    update_all_files() 