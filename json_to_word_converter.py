from docx import Document
from docx.shared import Pt, RGBColor, Inches
import json
from tqdm import tqdm

class JsonToWordConverter:
    def __init__(self):
        self.document = Document()
        self.current_level = 0
        
    def format_heading(self, level):
        """Format heading based on level"""
        if level == 0:
            return self.document.styles['Heading 1']
        elif level == 1:
            return self.document.styles['Heading 2']
        else:
            return self.document.styles['Heading 3']

    def add_item(self, key, value, level=0):
        """Add item to document with proper indentation and formatting"""
        # Add indentation based on level
        indent = "    " * level
        
        if isinstance(value, dict):
            # Add category/key as heading
            heading = self.document.add_paragraph(style=self.format_heading(level))
            heading.add_run(f"{key}").bold = True
            
            # Recursively process nested dictionary
            for sub_key, sub_value in value.items():
                self.add_item(sub_key, sub_value, level + 1)
                
        elif isinstance(value, list):
            # Add category/key as heading
            heading = self.document.add_paragraph(style=self.format_heading(level))
            heading.add_run(f"{key}").bold = True
            
            # Process list items
            for idx, item in enumerate(value):
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        self.add_item(sub_key, sub_value, level + 1)
                else:
                    p = self.document.add_paragraph()
                    p.paragraph_format.left_indent = Inches(level * 0.5)
                    p.add_run(f"• {str(item)}")
        else:
            # Add key-value pair as regular text
            p = self.document.add_paragraph()
            p.paragraph_format.left_indent = Inches(level * 0.5)
            p.add_run(f"{key}: ").bold = True
            p.add_run(str(value))

    def process_list(self, data_list, level=0):
        """Process a list of items"""
        for idx, item in enumerate(tqdm(data_list, desc="Converting")):
            if isinstance(item, dict):
                for key, value in item.items():
                    self.add_item(key, value, level)
            else:
                p = self.document.add_paragraph()
                p.paragraph_format.left_indent = Inches(level * 0.5)
                p.add_run(f"• {str(item)}")

    def process_dict(self, data_dict, level=0):
        """Process a dictionary"""
        for key, value in tqdm(data_dict.items(), desc="Converting"):
            self.add_item(key, value, level)

    def convert(self, input_json_path, output_docx_path):
        """Convert JSON file to Word document"""
        # Read JSON file
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add title
        title = self.document.add_heading('JSON Structure', 0)
        
        # Process JSON data based on its type
        if isinstance(data, list):
            self.process_list(data)
        elif isinstance(data, dict):
            self.process_dict(data)
        
        # Save document
        self.document.save(output_docx_path)
        print(f"Document saved successfully to {output_docx_path}") 