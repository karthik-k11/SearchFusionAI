import faiss
import numpy as np


def build_faiss_index(embeddings):

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_faiss(
    model,
    index,
    chunks,
    query,
    top_k=5
):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx != -1 and distance < 2.0:

            results.append(
                (
                    chunks[idx],
                    float(distance)
                )
            )

    return results