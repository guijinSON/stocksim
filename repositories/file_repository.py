import json
import logging
import os

logger = logging.getLogger(__name__)


class FileRepository:
    def __init__(self, path: str) -> None:
        self._base_path = path

    def create_or_overwrite_file(self, filepath: str):
        directory = os.path.dirname(f"{self._base_path}/{filepath}")

        if not os.path.exists(directory):
            os.makedirs(directory)

    def create_or_append_file(self, filepath: str, content):
        directory = os.path.dirname(f"{self._base_path}/")
        os.makedirs(directory, exist_ok=True)

        with open(f"{directory}/{filepath}", 'a') as file:
            file.write(content + "\n")

    def write_file(self, filename: str, data: dict):
        self.create_or_overwrite_file(filename)
        with open(f"{self._base_path}/{filename}", "w") as json_file:
            json.dump(data, json_file)

    def read_file(self, filename, file_type: str = "json"):
        try:
            full_path: str = f"{self._base_path}/{filename}.{file_type}"
            if file_type == "json":
                with open(full_path, "r") as json_file:
                    data = json.load(json_file)
            if file_type == "lxml":
                with open(full_path, "r") as html_file:
                    data = html_file.read()
            if file_type == "md":
                with open(full_path, "r", encoding="utf-8") as markdown_file:
                    data = markdown_file.read()
            return data
        except FileNotFoundError:
            print(f"Error: The file '{filename}' does not exist.")
            return None
