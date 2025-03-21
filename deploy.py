import os
import shutil
import json
import subprocess
import argparse

def export_schemas(output_dir='docs'):
    """Export schemas from MongoDB to static JSON files."""
    print("Exporting schemas from MongoDB...")
    try:
        # Run the export_schemas.py script with docs as the output directory
        subprocess.run(['python', 'export_schemas.py', '--out', output_dir], check=True)
        print("Schema export completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error exporting schemas: {e}")
        print("Continuing with deployment...")

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def copy_file(src, dst):
    """Copy a file and create parent directories if needed"""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"Copied {src} to {dst}")

def deploy_to_github_pages():
    try:
        # Create docs directory if it doesn't exist
        ensure_directory_exists('docs')
        
        # Copy main files
        files_to_copy = [
            'index.html',
            'categories_en.json',
            'categories_de.json',
            'styles.css',
            'script.js'
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                copy_file(file, f'docs/{file}')
        
        # Ensure schema directories exist
        ensure_directory_exists('docs/schemas_en')
        ensure_directory_exists('docs/schemas_de')
        
        # Create GitHub Pages specific files
        with open('docs/.nojekyll', 'w') as f:
            pass  # Empty file to prevent Jekyll processing
        
        # Create a simple 404 page
        with open('docs/404.html', 'w') as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>404 - Page Not Found</title>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>The requested page could not be found.</p>
    <a href="/">Return to Home</a>
</body>
</html>
""")
        
        print("Deployment preparation completed successfully!")
        print("\nNext steps:")
        print("1. Commit all changes in the 'docs' directory")
        print("2. Push to GitHub")
        print("3. Enable GitHub Pages in repository settings:")
        print("   - Go to Settings > Pages")
        print("   - Set source to 'Deploy from a branch'")
        print("   - Select 'main' branch and '/docs' folder")
        print("   - Save")
        
    except Exception as e:
        print(f"Error during deployment preparation: {e}")

if __name__ == '__main__':
    deploy_to_github_pages() 