import json

def verify_categories():
    languages = ['en', 'de']
    
    for lang in languages:
        try:
            filename = f'categories_{lang}.json'
            print(f"\nVerifying {filename}:")
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            print(f"Found {len(data)} categories:")
            for category in data:
                print(f"\n{category['name']} (Code: {category['code']}):")
                print(f"- {len(category['subcategories'])} subcategories")
                sub_sub_count = sum(len(sub.get('subSubcategories', [])) 
                                  for sub in category['subcategories'])
                print(f"- {sub_sub_count} sub-subcategories")
                
        except FileNotFoundError:
            print(f"Warning: {filename} not found")
        except Exception as e:
            print(f"Error verifying {filename}: {e}")

if __name__ == "__main__":
    verify_categories() 