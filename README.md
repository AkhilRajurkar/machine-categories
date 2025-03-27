# Machine Categories Browser

A web application for browsing machine categories with MongoDB schema integration. The application can run both locally and on GitHub Pages.

## Features

- Browse machine categories in a hierarchical structure
- View sub-subcategory schemas from MongoDB
- Support for both English and German languages
- Works on both local development and GitHub Pages

## Prerequisites

- Python 3.7+
- MongoDB access (for local development and schema export)
- Git (for deployment to GitHub Pages)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AkhilRajurkar/machine-categories.git
   cd machine-categories
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Local Development

1. Start the local Flask server:
   ```
   python server.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## GitHub Pages Deployment

The application is designed to work on GitHub Pages by using static JSON files for schemas instead of a live MongoDB connection.

### Exporting Schemas for GitHub Pages

1. Export schemas from MongoDB to static JSON files:
   ```
   python export_schemas.py
   ```

   This will create two directories:
   - `schemas_en/` - English schemas
   - `schemas_de/` - German schemas

2. Deploy all necessary files to the `docs/` directory:
   ```
   python deploy.py
   ```

   This will:
   - Export schemas from MongoDB (if not previously exported)
   - Copy necessary files to the `docs/` directory
   - Create schema directories if they don't exist

3. Commit and push the changes to GitHub:
   ```
   git add docs/
   git commit -m "Update GitHub Pages deployment"
   git push
   ```

4. Enable GitHub Pages in repository settings:
   - Go to your repository on GitHub
   - Navigate to Settings > Pages
   - Set source to "Deploy from a branch"
   - Select "main" branch and "/docs" folder
   - Save

### Deployment Options

- To skip schema export during deployment (if you've already exported them):
  ```
  python deploy.py --skip-schemas
  ```

## Customization

- MongoDB connection:
  - The connection string is in `server.py` for local development
  - The connection string is in `export_schemas.py` for schema export

- Styling:
  - Edit the CSS in `index.html` to customize the appearance

## File Structure

- `server.py` - Flask server for local development
- `index.html` - Main web application
- `export_schemas.py` - Tool to export MongoDB schemas to static files
- `deploy.py` - Deployment script for GitHub Pages
- `schemas_en/` - Directory for English schemas
- `schemas_de/` - Directory for German schemas
- `docs/` - GitHub Pages deployment directory
