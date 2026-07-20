from flask import Flask, render_template, request
import os

from extractor import extract_text
from chunker import create_chunks
from bm25_engine import build_bm25, search_bm25
from embedding_engine import generate_embeddings, model
from faiss_engine import build_faiss_index, search_faiss
from rrf_engine import reciprocal_rank_fusion
from db import create_database, save_search, get_history, clear_history

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

all_chunks = []

all_file_names = []

current_bm25 = None

current_embeddings = None

current_faiss_index = None

current_preview_text = ""
current_file_name = ""
current_character_count = 0

embedding_count = 0

create_database()


@app.route("/", methods=["GET", "POST"])
def home():

    global all_chunks
    global all_file_names
    global current_bm25
    global current_embeddings
    global current_faiss_index

    global current_preview_text
    global current_file_name
    global current_character_count

    global embedding_count

    preview_text = current_preview_text
    chunks = all_chunks
    file_name = current_file_name
    character_count = current_character_count

    message = ""

    bm25_results = []
    semantic_results = []
    hybrid_results = []

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

            current_faiss_index = build_faiss_index(
                current_embeddings
            )

            embedding_count = len(current_embeddings)

            all_chunks.extend(chunks)
            current_preview_text = preview_text
            current_file_name = uploaded_file.filename
            current_character_count = len(preview_text)

            preview_text = current_preview_text
            chunks = all_chunks
            file_name = current_file_name
            character_count = current_character_count

            bm25_ready = True
            message = "Document uploaded successfully."

    query = request.args.get(
        "query",
        ""
    ).strip()

    if (
        query
        and current_bm25
        and current_faiss_index
    ):

        bm25_results = search_bm25(
            current_bm25,
            all_chunks,
            query
        )

        semantic_results = search_faiss(
            model,
            current_faiss_index,
            all_chunks,
            query
        )

        hybrid_results = reciprocal_rank_fusion(
            bm25_results,
            semantic_results
        )

        save_search(
            query,
            current_file_name,
            len(hybrid_results)
        )

        preview_text = current_preview_text
        chunks = all_chunks
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

        query=query,

        embedding_count=embedding_count,

        faiss_ready=current_faiss_index is not None,

        results=bm25_results,

        semantic_results=semantic_results,

        hybrid_results=hybrid_results
    )


@app.route("/history")
def history():

    history = get_history()

    return render_template(
        "history.html",
        history=history
    )

@app.route("/clear-history")
def clear_all_history():

    clear_history()

    history = get_history()

    return render_template(
        "history.html",
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)