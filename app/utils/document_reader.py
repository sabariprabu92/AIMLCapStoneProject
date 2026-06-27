import json
import pandas as pd
import yaml
from PyPDF2 import PdfReader


def extract_text_from_file(file_path: str, file_extension: str) -> str:
    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if file_extension == ".txt":
        return extract_text_from_txt(file_path)

    if file_extension == ".csv":
        return extract_text_from_csv(file_path)

    if file_extension in [".xlsx", ".xls"]:
        return extract_text_from_excel(file_path)

    if file_extension == ".json":
        return extract_text_from_json(file_path)

    if file_extension in [".yaml", ".yml"]:
        return extract_text_from_yaml(file_path)

    return ""


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def extract_text_from_csv(file_path: str) -> str:
    df = pd.read_csv(file_path)
    return df.to_string(index=False)


def extract_text_from_excel(file_path: str) -> str:
    df = pd.read_excel(file_path)
    return df.to_string(index=False)


def extract_text_from_json(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        data = json.load(file)

    return json.dumps(data, indent=2)


def extract_text_from_yaml(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        data = yaml.safe_load(file)

    return yaml.dump(data)