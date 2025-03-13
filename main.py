from json_to_word_converter import JsonToWordConverter

def main():
    # Initialize converter
    converter = JsonToWordConverter()
    
    # Define input and output paths
    input_json = "categories_coded.json"
    output_docx = "categories_coded.docx"
    
    # Convert JSON to Word
    converter.convert(input_json, output_docx)

if __name__ == "__main__":
    main()
