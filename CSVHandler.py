import csv
import os

class CSVHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def create_file_with_headers(self, headers: list[str]) -> tuple[int, str]:
        try:
            if not isinstance(headers, list) or not all(isinstance(h, str) for h in headers):
                raise ValueError("Headers must be a list of strings.")

            with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
            return 200, "File created successfully."

        except Exception as e:
            return 201, f"Error creating file: {e}"

    def append_dict_of_dicts(self, data: dict) -> tuple[int, str]:
        try:
            if not isinstance(data, dict) or not all(isinstance(v, dict) for v in data.values()):
                raise ValueError("Data must be a dictionary of dictionaries.")

            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"{self.file_path} does not exist. Please create it first.")

            # Get existing headers
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames

            if not headers:
                raise ValueError("CSV file has no headers.")

            with open(self.file_path, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
                for inner_dict in data.values():
                    row = {key: inner_dict.get(key, "") for key in headers}
                    writer.writerow(row)

            return 200, "Data appended successfully."

        except Exception as e:
            return 201, f"Error appending data: {e}"

    def wipe_all_rows(self) -> tuple[int, str]:
        """
        Removes all data rows from the CSV but keeps the header.
        """
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"{self.file_path} does not exist.")

            with open(self.file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None)

            if not headers:
                raise ValueError("CSV file has no header to preserve.")

            with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

            return 200, "All rows wiped, header preserved."

        except Exception as e:
            return 201, f"Error wiping rows: {e}"

    def read_all_rows(self) -> tuple[int, str]:
        """
        Reads and prints all rows in the CSV (excluding the header).
        """
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"{self.file_path} does not exist.")

            with open(self.file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                print(f"Headers: {headers}")
                for row in reader:
                    print(row)

            return 200, "Rows printed successfully."

        except Exception as e:
            return 201, f"Error reading rows: {e}"
