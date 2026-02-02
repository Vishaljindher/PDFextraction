from flask import Flask, request, jsonify
import os
import uuid
from flask_cors import CORS

from core.file_loader import load_file
from core.text_cleaner import clean_text
from core.question_parser import extract_questions
from core.output_formatter import format_output

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/extract-questions", methods=["POST"])
def extract_questions_api():
    # 1️⃣ File validation
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file or file.filename.strip() == "":
        return jsonify({"error": "Empty filename"}), 400

    # 2️⃣ Save uploaded file with unique name
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # 3️⃣ Run extraction pipeline
        raw_text = load_file(file_path)
        cleaned_text = clean_text(raw_text)
        questions = extract_questions(cleaned_text)

        formatted_questions = []

        for q in questions:
            formatted_questions.append(
                format_output(
                    question=q.get("question"),
                    q_type=q.get("type", "unknown"),
                    difficulty=q.get("difficulty", "unknown"),
                    source=file.filename,
                    options=q.get("options", {}),
                    answer=q.get("answer")
                )
            )

        # 4️⃣ Success response
        return jsonify({
            "total": len(formatted_questions),
            "questions": formatted_questions
        })

    except Exception as e:
        # 5️⃣ Error handling
        return jsonify({
            "error": "Failed to process file",
            "details": str(e)
        }), 500

    finally:
        # 6️⃣ Optional: cleanup uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

