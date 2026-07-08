def reciprocal_rank_fusion(
    bm25_results,
    semantic_results,
    k=60
):

    fused_scores = {}

    chunk_lookup = {}

    for rank, (chunk, _) in enumerate(bm25_results):

        score = 1 / (k + rank + 1)

        fused_scores[chunk] = fused_scores.get(chunk, 0) + score

        chunk_lookup[chunk] = chunk

    for rank, (chunk, _) in enumerate(semantic_results):

        score = 1 / (k + rank + 1)

        fused_scores[chunk] = fused_scores.get(chunk, 0) + score

        chunk_lookup[chunk] = chunk

    ranked = sorted(

        fused_scores.items(),

        key=lambda x: x[1],

        reverse=True

    )

    results = []

    for chunk, score in ranked:

        results.append(

            (chunk_lookup[chunk], score)

        )

    return results