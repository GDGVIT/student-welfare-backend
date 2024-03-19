import csv


def validate_csv(csv_file):
    if not csv_file:
        return False, "No file found"
    if not csv_file.name.endswith(".csv"):
        return False, "Invalid file type"
    if csv_file.multiple_chunks():
        return False, "File too large"
    return True, None


def process_csv(file, required_columns, columns, process_data_func):
    validity, error = validate_csv(file)
    if not validity:
        return False, error

    responses = {
        "success": [],
        "failure": [],
    }

    reader = csv.DictReader(file.read().decode("utf-8").splitlines())
    for row in reader:
        row_data = {}
        for col in columns:
            header = col.replace(" ", "").lower()
            if header in row:
                row_data[col] = row[header]
            else:
                if col in required_columns:
                    return False, f"Required column '{col}' not found in CSV file"
                else:
                    row_data[col] = None

        try:
            process_data_func(row_data, responses)
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})

    return True, responses