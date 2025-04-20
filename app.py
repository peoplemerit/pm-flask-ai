from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import sys  # <-- ADD THIS
# Explicit path for Tesseract on Render
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ PMERIT server is running cleanly!"

@app.route("/upload-image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        image = Image.open(file)
        extracted_text = pytesseract.image_to_string(image)
        return jsonify({"extracted_text": extracted_text})
    except Exception as e:
        print(f"OCR error: {e}", file=sys.stderr)  # <== log error to Render
        return jsonify({"error": str(e)}), 500
