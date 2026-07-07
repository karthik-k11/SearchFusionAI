from rank_bm25 import BM25Okapi


def build_bm25(chunks):

    tokenized_chunks = [chunk.lower().split() for chunk in chunks]

    bm25 = BM25Okapi(tokenized_chunks)

    return bm25


def search_bm25(bm25, chunks, query, top_k=5):

    query = query.lower().strip()

    scores = bm25.get_scores(query.split())

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    query_words = set(query.split())

    for chunk, score in ranked:

        chunk_words = set(chunk.lower().split())

        if query_words.intersection(chunk_words):

            results.append((chunk, score))

    return results[:top_k]