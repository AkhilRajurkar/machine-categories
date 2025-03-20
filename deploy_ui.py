import os
import shutil
import json

def deploy_ui():
    # Create docs directory if it doesn't exist
    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    # Files to copy to docs
    files = [
        'index.html',
        'categories_en.json',
        'categories_de.json'
    ]
    
    # Copy files
    for file in files:
        if os.path.exists(file):
            shutil.copy2(file, f'docs/{file}')
            print(f"Copied {file} to docs/")
        else:
            print(f"Warning: {file} not found")
    
    # Verify categories files content
    for lang in ['en', 'de']:
        try:
            with open(f'docs/categories_{lang}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"\nVerified categories_{lang}.json contains {len(data)} categories:")
                for cat in data:
                    print(f"- {cat['code']}: {cat['name']}")
        except Exception as e:
            print(f"Error verifying categories_{lang}.json: {e}")
    
    print("\nDeployment ready! Next steps:")
    print("1. Commit and push the changes to GitHub")
    print("2. Go to repository settings")
    print("3. Under GitHub Pages, set source to 'docs' folder")
    print("4. Your site will be available at: https://[username].github.io/[repo-name]/")

if __name__ == "__main__":
    deploy_ui() 