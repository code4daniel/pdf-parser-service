from flask import Flask, request, jsonify
from utils.pdf_extractor import extract_cutoffs_from_pdf
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/parse', methods=['POST'])
def parse_pdf():
    if 'pdf' not in request.files or 'university' not in request.form:
        return jsonify({"error": "Missing file or university name"}), 400

    pdf_file = request.files['pdf']
    university = request.form['university']
    file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(file_path)

    try:
        data = extract_cutoffs_from_pdf(file_path, university)
        return jsonify({"cutoffs": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
