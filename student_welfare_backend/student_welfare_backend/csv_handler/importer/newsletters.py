from datetime import datetime

from student_welfare_backend.core.models import Newsletter

class NewslettersCSVImporter:
    STANDARD_FIELDS = [
        "link",
        "cover_page",
        "month",
        "year"
    ]
    
    REQUIRED_FIELDS = [
        "link",
        "month",
        "year",
    ]
    
    def process_csv_func(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.REQUIRED_FIELDS if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
            
            month1 = row_data["month"].lower()
        
            # Check if the type is valid
            if month1 not in dict(Newsletter.month_names).keys():
                raise ValueError(f"Invalid type: {month1}")
            # Create special file
            newsletter = Newsletter.objects.update_or_create(
                year=row_data["year"],
                month=month1,
                cover_page=row_data["cover_page"],
                link=row_data["link"],
            )
            
            responses["success"].append({"row": row_data, "detail": "Newsletter created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})