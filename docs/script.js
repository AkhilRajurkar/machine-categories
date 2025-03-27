// Machine Categories Browser Script
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
