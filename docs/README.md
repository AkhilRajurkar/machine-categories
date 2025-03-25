# Machine Categories Browser

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
