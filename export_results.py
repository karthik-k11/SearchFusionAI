import csv


def export_to_csv(results):

    with open(
        "search_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Source File",
                "Hybrid Score",
                "Content"
            ]
        )

        for chunk, score, source_file in results:

            writer.writerow(
                [
                    source_file,
                    score,
                    chunk
                ]
            )