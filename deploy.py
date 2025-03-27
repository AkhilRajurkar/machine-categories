import os
import shutil
import json
import subprocess
import argparse

def export_schemas(output_dir='docs'):
    """Export schemas from MongoDB to static JSON files."""
    print("Exporting schemas from MongoDB...")
    try:
        # Get the current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        export_script = os.path.join(script_dir, 'export_schemas.py')
        
        # Run the export_schemas.py script with docs as the output directory
        subprocess.run(['python', export_script, '--out', output_dir], check=True)
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
    # Check if the source is an absolute path or if it needs to be resolved relative to script dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # First try the source as is
    if os.path.exists(src):
        file_src = src
    # Then try relative to the script directory
    elif os.path.exists(os.path.join(script_dir, src)):
        file_src = os.path.join(script_dir, src)
    else:
        print(f"Warning: Source file '{src}' not found, skipping")
        return
    
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(file_src, dst)
    print(f"Copied {file_src} to {dst}")

def deploy_to_github_pages():
    try:
        # Create docs directory if it doesn't exist
        ensure_directory_exists('docs')
        
        # Export schemas first
        export_schemas('docs')
        
        # Get script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Copy main files
        files_to_copy = [
            'index.html',
            'categories_en.json',
            'categories_de.json',
            'server.py',  # Include server.py for API endpoints
            'requirements.txt'  # Include requirements.txt for dependencies
        ]
        
        for file in files_to_copy:
            copy_file(file, f'docs/{file}')
        
        # Create or update CSS file if it doesn't exist
        css_file = os.path.join(script_dir, 'docs', 'styles.css')
        if not os.path.exists(css_file):
            print(f"Creating styles.css file...")
            with open(css_file, 'w') as f:
                f.write("""/* Machine Categories Browser Styles */
body {
    font-family: Arial, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f8f9fa;
}
.container {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}
.category-section {
    flex: 1;
    padding: 15px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.category-item {
    cursor: pointer;
    padding: 10px;
    margin: 5px 0;
    border-radius: 6px;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}
.category-item:hover {
    background-color: #f0f0f0;
    border-color: #ddd;
}
.selected {
    background-color: #e3f2fd;
    color: #1976d2;
    border-color: #90caf9;
}
.language-selector {
    text-align: right;
    margin-bottom: 20px;
}
.language-selector button {
    padding: 8px 16px;
    margin-left: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.language-selector button.active {
    background-color: #1976d2;
    color: white;
    border-color: #1976d2;
}
""")
        
        # Create or update JS file if it doesn't exist
        js_file = os.path.join(script_dir, 'docs', 'script.js')
        if not os.path.exists(js_file):
            print(f"Creating script.js file...")
            with open(js_file, 'w') as f:
                f.write("""// Machine Categories Browser Script
document.addEventListener('DOMContentLoaded', function() {
    // Default language
    let currentLanguage = 'en';
    
    // Set language buttons event listeners
    document.getElementById('btn-en').addEventListener('click', () => setLanguage('en'));
    document.getElementById('btn-de').addEventListener('click', () => setLanguage('de'));
    
    // Initial load
    loadCategories(currentLanguage);
    
    // Function to set language and update UI
    function setLanguage(lang) {
        currentLanguage = lang;
        
        // Update active button
        document.querySelectorAll('.language-selector button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(`btn-${lang}`).classList.add('active');
        
        // Reload categories
        loadCategories(lang);
        
        // Clear subcategories and sub-subcategories
        document.getElementById('subcategories').innerHTML = '<div class="empty-message">Select a main category</div>';
        document.getElementById('sub-subcategories').innerHTML = '<div class="empty-message">Select a subcategory</div>';
        
        // Clear schema
        document.getElementById('schema-info').innerHTML = '';
    }
    
    // Function to load categories
    function loadCategories(lang) {
        fetch(`categories_${lang}.json`)
            .then(response => response.json())
            .then(data => {
                displayCategories(data);
            })
            .catch(error => {
                console.error('Error loading categories:', error);
                document.getElementById('main-categories').innerHTML = 
                    `<div class="error-message">Error loading categories. Please try again later.</div>`;
            });
    }
    
    // Function to display main categories
    function displayCategories(categories) {
        const container = document.getElementById('main-categories');
        container.innerHTML = '';
        
        categories.forEach(category => {
            const div = document.createElement('div');
            div.className = 'category-item';
            div.setAttribute('data-code', category.code);
            div.innerHTML = `${category.name} <span class="code">${category.code}</span>`;
            
            div.addEventListener('click', function() {
                // Highlight selected
                document.querySelectorAll('#main-categories .category-item').forEach(item => {
                    item.classList.remove('selected');
                });
                this.classList.add('selected');
                
                // Display subcategories
                displaySubcategories(category.subcategories);
                
                // Clear sub-subcategories
                document.getElementById('sub-subcategories').innerHTML = 
                    '<div class="empty-message">Select a subcategory</div>';
                
                // Clear schema
                document.getElementById('schema-info').innerHTML = '';
            });
            
            container.appendChild(div);
        });
    }
    
    // Function to display subcategories
    function displaySubcategories(subcategories) {
        const container = document.getElementById('subcategories');
        container.innerHTML = '';
        
        if (!subcategories || subcategories.length === 0) {
            container.innerHTML = '<div class="empty-message">No subcategories available</div>';
            return;
        }
        
        subcategories.forEach(subcategory => {
            const div = document.createElement('div');
            div.className = 'category-item';
            div.setAttribute('data-code', subcategory.code);
            div.innerHTML = `${subcategory.name} <span class="code">${subcategory.code}</span>`;
            
            div.addEventListener('click', function() {
                // Highlight selected
                document.querySelectorAll('#subcategories .category-item').forEach(item => {
                    item.classList.remove('selected');
                });
                this.classList.add('selected');
                
                // Display sub-subcategories
                displaySubSubcategories(subcategory.sub_subcategories);
            });
            
            container.appendChild(div);
        });
    }
    
    // Function to display sub-subcategories
    function displaySubSubcategories(subSubcategories) {
        const container = document.getElementById('sub-subcategories');
        container.innerHTML = '';
        
        if (!subSubcategories || subSubcategories.length === 0) {
            container.innerHTML = '<div class="empty-message">No sub-subcategories available</div>';
            return;
        }
        
        subSubcategories.forEach(subSubcat => {
            const div = document.createElement('div');
            div.className = 'category-item';
            div.setAttribute('data-code', subSubcat.code);
            div.innerHTML = `${subSubcat.name} <span class="code">${subSubcat.code}</span>`;
            
            div.addEventListener('click', function() {
                // Highlight selected
                document.querySelectorAll('#sub-subcategories .category-item').forEach(item => {
                    item.classList.remove('selected');
                });
                this.classList.add('selected');
                
                // Load schema
                loadSchema(subSubcat.code, currentLanguage);
            });
            
            container.appendChild(div);
        });
    }
    
    // Function to load schema
    function loadSchema(code, lang) {
        const schemaContainer = document.getElementById('schema-info');
        schemaContainer.innerHTML = '<div class="schema-loading">Loading schema information...</div>';
        
        fetch(`schemas_${lang}/${code}.json`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Schema not found');
                }
                return response.json();
            })
            .then(data => {
                displaySchema(data);
            })
            .catch(error => {
                console.error('Error loading schema:', error);
                schemaContainer.innerHTML = 
                    `<div class="schema-error">Error loading schema information. The schema may not exist yet.</div>`;
            });
    }
    
    // Function to display schema
    function displaySchema(schema) {
        const container = document.getElementById('schema-info');
        container.innerHTML = '';
        
        // Create schema title
        const title = document.createElement('div');
        title.className = 'schema-title';
        title.textContent = currentLanguage === 'en' ? 
            `Schema for ${schema.sub_subcategory || 'Unknown'}` : 
            `Schema für ${schema.unterunterkategorie || 'Unbekannt'}`;
        container.appendChild(title);
        
        // Display schema information
        if (schema.schema) {
            // Display required fields
            if (schema.schema.required && schema.schema.required.length > 0) {
                const requiredSection = document.createElement('div');
                requiredSection.innerHTML = `<strong>Required Fields:</strong> ${schema.schema.required.join(', ')}`;
                container.appendChild(requiredSection);
            }
            
            // Display properties
            if (schema.schema.properties) {
                const propsTable = document.createElement('table');
                propsTable.className = 'schema-table';
                
                // Table header
                const thead = document.createElement('thead');
                thead.innerHTML = `
                    <tr>
                        <th>Property</th>
                        <th>Type</th>
                        <th>Description</th>
                    </tr>
                `;
                propsTable.appendChild(thead);
                
                // Table body
                const tbody = document.createElement('tbody');
                
                for (const [propName, propDetails] of Object.entries(schema.schema.properties)) {
                    const row = document.createElement('tr');
                    
                    // Property name
                    const nameCell = document.createElement('td');
                    nameCell.textContent = propName;
                    
                    // Add required badge if needed
                    if (schema.schema.required && schema.schema.required.includes(propName)) {
                        const badge = document.createElement('span');
                        badge.className = 'required-badge';
                        badge.textContent = 'Required';
                        nameCell.appendChild(badge);
                    }
                    
                    row.appendChild(nameCell);
                    
                    // Property type
                    const typeCell = document.createElement('td');
                    if (propDetails.bsonType) {
                        const type = Array.isArray(propDetails.bsonType) ? 
                            propDetails.bsonType.join(' | ') : propDetails.bsonType;
                        
                        const typeBadge = document.createElement('span');
                        typeBadge.className = 'type-badge';
                        typeBadge.textContent = type;
                        typeCell.appendChild(typeBadge);
                    } else {
                        typeCell.textContent = 'N/A';
                    }
                    row.appendChild(typeCell);
                    
                    // Description and constraints
                    const descCell = document.createElement('td');
                    
                    // Add description if exists
                    if (propDetails.description) {
                        descCell.textContent = propDetails.description;
                    }
                    
                    // Add enum values if they exist
                    if (propDetails.enum && propDetails.enum.length > 0) {
                        const enumDiv = document.createElement('div');
                        enumDiv.className = 'enum-values';
                        enumDiv.textContent = `Values: ${propDetails.enum.join(', ')}`;
                        descCell.appendChild(enumDiv);
                    }
                    
                    row.appendChild(descCell);
                    tbody.appendChild(row);
                }
                
                propsTable.appendChild(tbody);
                container.appendChild(propsTable);
            }
        } else {
            container.innerHTML += '<div class="schema-error">Schema structure not found</div>';
        }
    }
});
""")
        
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
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #1976d2;
        }
        a {
            color: #1976d2;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>The requested page could not be found.</p>
    <a href="/">Return to Home</a>
</body>
</html>
""")
        
        # Create a README.md in the docs directory
        with open('docs/README.md', 'w') as f:
            f.write("""# Machine Categories Browser

This is the deployed version of the Machine Categories Browser application.

## Features
- Browse machine categories in English and German
- View detailed schema information
- SEO tags for better searchability
- Manufacturer information including European certifications
- Responsive design for all devices

## API Endpoints
- `/api/categories/<language>` - Get categories for specified language
- `/api/schema/<language>/<code>` - Get schema information for a specific category code

## Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `python server.py`
3. Open http://localhost:5000 in your browser
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