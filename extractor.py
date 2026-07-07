from PyPDF2 import PdfReader


def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8")


def extract_text(file_path):

    if file_path.lower().endswith(".txt"):

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return clean_text(file.read())

    elif file_path.lower().endswith(".pdf"):

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return clean_text(text)

    else:

        return "Unsupported file format."