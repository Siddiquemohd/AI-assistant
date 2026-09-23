import csv
import json
import os

class DocumentParserEngine:
    """
    Document, CSV, JSON & Text Data Analysis Engine.
    Parses structural data files, calculates summary metrics, and performs file analysis.
    """

    def analyze_file(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {"status": "Error", "error": f"File '{file_path}' does not exist."}

        file_ext = os.path.splitext(file_path)[1].lower()

        try:
            if file_ext == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    key_count = len(data) if isinstance(data, (dict, list)) else 1
                    return {
                        "status": "Success",
                        "type": "JSON Data Document",
                        "file_path": file_path,
                        "structure": type(data).__name__,
                        "element_count": key_count,
                        "preview": str(data)[:300]
                    }

            elif file_ext == ".csv":
                with open(file_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    header = rows[0] if rows else []
                    return {
                        "status": "Success",
                        "type": "CSV Tabular Dataset",
                        "file_path": file_path,
                        "headers": header,
                        "row_count": len(rows) - 1 if len(rows) > 0 else 0,
                        "column_count": len(header)
                    }

            else:
                # Text / Markdown file
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    line_count = len(content.splitlines())
                    word_count = len(content.split())
                    return {
                        "status": "Success",
                        "type": "Text / Markdown Document",
                        "file_path": file_path,
                        "line_count": line_count,
                        "word_count": word_count,
                        "preview": content[:300]
                    }

        except Exception as e:
            return {"status": "Error", "file_path": file_path, "error": str(e)}
