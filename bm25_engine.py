from rank_bm25 import BM25Okapi


def build_bm25(chunks):

    tokenized_chunks = []

    for chunk in chunks:
        tokenized_chunks.append(chunk.lower().split())

    bm25 = BM25Okapi(tokenized_chunks)

    return bm25