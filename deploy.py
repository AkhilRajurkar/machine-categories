import os
import shutil
import json

def deploy_for_github_pages():
    # Files needed for GitHub Pages
    files_to_deploy = [
        'index.html',
        'categories_en.json',
        'categories_de.json'
    ]
    
    # Create docs directory if it doesn't exist
    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    # Copy necessary files to docs
    for file in files_to_deploy:
        if os.path.exists(file):
            shutil.copy2(file, f'docs/{file}')
            print(f"Copied {file} to docs/")
        else:
            print(f"Warning: {file} not found")
    
    print("\nDeployment files ready in 'docs' directory")
    print("Next steps:")
    print("1. Commit and push the changes to GitHub")
    print("2. Enable GitHub Pages in repository settings (if not already enabled)")
    print("3. Set source to 'docs' folder in GitHub Pages settings")

if __name__ == "__main__":
    deploy_for_github_pages() 