from flask import Flask, render_template, request
import os

from extractor import extract_text
from chunker import create_chunks
from bm25_engine import build_bm25

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():

    preview_text = ""
    chunks = []
    bm25_ready = False

    file_name = ""
    character_count = 0

    message = ""

    if request.method == "POST":

        uploaded_file = request.files.get("document")

        if uploaded_file and uploaded_file.filename != "":

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                uploaded_file.filename
            )

            uploaded_file.save(file_path)

            preview_text = extract_text(file_path)

            chunks = create_chunks(preview_text)

            bm25 = build_bm25(chunks)

            file_name = uploaded_file.filename

            character_count = len(preview_text)

            message = "Document uploaded successfully."
            bm25_ready = True

        else:

            message = "Please choose a file."

    return render_template(
        "index.html",
        preview_text=preview_text,
        chunks=chunks,
        file_name=file_name,
        character_count=character_count,
        message=message,
        bm25_ready=bm25_ready
    )


if __name__ == "__main__":
    app.run(debug=True)