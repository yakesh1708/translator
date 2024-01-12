
import os
from PIL import Image
import pytesseract
from flask import Flask, request, render_template, jsonify
from translate import Translator
import html

app = Flask(__name__)

# Define path to Tesseract executable
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Point pytesseract to Tesseract executable
pytesseract.pytesseract_cmd = path_to_tesseract

# Create a folder to store uploaded images
upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the uploaded image file
        image_file = request.files['image']
        src_language = request.form['target_language']
        target_language = request.form['target_language']

        if image_file:
            # Save the uploaded image to the 'uploads' folder
            image_path = os.path.join(upload_folder, image_file.filename)
            image_file.save(image_path)

            try:
                # Open the uploaded image using PIL
                img = Image.open(image_path)

                # Extract text from the image using Tesseract
                extracted_text = pytesseract.image_to_string(img)

                # Translate the extracted text to the target language
                try:
                    translator = Translator(to_lang=target_language)
                    translated_text = translator.translate(extracted_text)

                    translator = Translator()
                    translated=translator.translate(text=extracted_text , src = src_language, dest = target_language)

                    # Decode HTML entities in the translated text
                    translated_text = translated

                except Exception as e:
                    return jsonify({'error': f"Error translating text: {str(e)}"})

            except Exception as e:
                return jsonify({'error': f"Error extracting text: {str(e)}"})

            # Encode the text as UTF-8 for human-readable output
            extracted_text = extracted_text.encode('utf-8').decode('utf-8')
            translated_text = translated_text

            return jsonify({'extracted_text': extracted_text, 'translated_text': translated_text})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
