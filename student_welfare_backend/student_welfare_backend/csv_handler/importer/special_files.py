from datetime import datetime

from student_welfare_backend.core.models import SpecialFile

class SpecialFilesCSVImporter:
    STANDARD_FIELDS = [
        "year",
        "file_link",
        "type"
    ]
    
    REQUIRED_FIELDS = [
        "year",
        "file_link",
        "type"
    ]
    
    def process_csv_func(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.REQUIRED_FIELDS if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
            
            file_type = row_data["type"]
            if file_type not in dict(SpecialFile.file_type_options).keys():
                raise ValueError(f"Invalid type: {file_type}")
            # Create special file
            special_file = SpecialFile.objects.update_or_create(
                year=row_data["year"],
                file_link=row_data["file_link"],
                type=file_type
            )
            
            responses["success"].append({"row": row_data, "detail": "Special file created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})