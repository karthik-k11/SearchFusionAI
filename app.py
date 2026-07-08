from flask import Flask, render_template, request
import os

from extractor import extract_text
from chunker import create_chunks
from bm25_engine import build_bm25, search_bm25
from embedding_engine import generate_embeddings

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

current_chunks = []
current_bm25 = None
current_file_name = ""
current_character_count = 0
current_preview_text = ""
current_embeddings = None
embedding_count = 0


@app.route("/", methods=["GET", "POST"])
def home():

    global current_chunks
    global current_bm25
    global current_file_name
    global current_character_count
    global current_preview_text
    global current_embeddings
    global embedding_count

    preview_text = current_preview_text
    chunks = current_chunks
    file_name = current_file_name
    character_count = current_character_count

    message = ""
    results = []
    bm25_ready = current_bm25 is not None

    if request.method == "POST":

        uploaded_file = request.files.get("document")

        if uploaded_file and uploaded_file.filename:

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                uploaded_file.filename
            )

            uploaded_file.save(file_path)

            preview_text = extract_text(file_path)

            chunks = create_chunks(preview_text)

            current_bm25 = build_bm25(chunks)
            current_embeddings = generate_embeddings(chunks)

            embedding_count = len(current_embeddings)

            current_chunks = chunks
            current_preview_text = preview_text
            current_file_name = uploaded_file.filename
            current_character_count = len(preview_text)

            preview_text = current_preview_text
            chunks = current_chunks
            file_name = current_file_name
            character_count = current_character_count

            bm25_ready = True
            message = "Document uploaded successfully."

    query = request.args.get("query", "").strip()

    if query and current_bm25:

        results = search_bm25(
            current_bm25,
            current_chunks,
            query
        )

        preview_text = current_preview_text
        chunks = current_chunks
        file_name = current_file_name
        character_count = current_character_count

    return render_template(
        "index.html",
        preview_text=preview_text,
        chunks=chunks,
        file_name=file_name,
        character_count=character_count,
        message=message,
        bm25_ready=bm25_ready,
        results=results,
        query=query,
        embedding_count=embedding_count
    )


if __name__ == "__main__":
    app.run(debug=True)