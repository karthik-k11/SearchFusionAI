from PyPDF2 import PdfReader


def extract_text(file_path):

    if file_path.lower().endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    elif file_path.lower().endswith(".pdf"):

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text

    else:

        return "Unsupported file format."