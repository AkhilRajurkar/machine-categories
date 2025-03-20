import json
import os

def verify_categories():
    expected_codes = set(range(1, 25))  # We expect codes 1-24
    found_codes = set()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "category_new", "english")
    
    print("Verifying categories...")
    
    for file in os.listdir(base_path):
        if file.endswith('_en.json'):
            with open(os.path.join(base_path, file), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    code = int(str(data['code']).split('.')[0])
                    found_codes.add(code)
                    print(f"Found category {code}: {data['name']}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    
    missing_codes = expected_codes - found_codes
    if missing_codes:
        print("\nMissing categories:")
        for code in sorted(missing_codes):
            print(f"Category {code} is missing")
    else:
        print("\nAll categories are present!")
    
    print(f"\nTotal categories found: {len(found_codes)}")

if __name__ == "__main__":
    verify_categories() 