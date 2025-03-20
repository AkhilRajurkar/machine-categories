import os
import json
import shutil

def create_german_file(en_file_path):
    # Get the German file path
    de_file_path = en_file_path.replace('/english/', '/german/').replace('_en.json', '_de.json')
    
    # Create German directory if it doesn't exist
    os.makedirs(os.path.dirname(de_file_path), exist_ok=True)
    
    # Copy English file as base
    shutil.copy2(en_file_path, de_file_path)
    print(f"Created German file: {de_file_path}")

def ensure_german_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    en_path = os.path.join(script_dir, "category_new", "english")
    
    for file in os.listdir(en_path):
        if file.endswith('_en.json'):
            en_file_path = os.path.join(en_path, file)
            de_file_path = en_file_path.replace('/english/', '/german/').replace('_en.json', '_de.json')
            
            if not os.path.exists(de_file_path):
                create_german_file(en_file_path)

if __name__ == "__main__":
    ensure_german_files() 