from student_welfare_backend.core.models import Club


class ClubsCSVImporter:
    STANDARD_FIELDS = [
        "name", 
        "type", 
        ""
        ]
    REQUIRED_FIELDS = ["name"]

    def process_csv_func(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.REQUIRED_FIELDS if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create club
            club = Club.objects.update_or_create(
                name=row_data["name"],
                is_chapter=bool(row_data.get("is_chapter", False)),
                is_technical=bool(row_data.get("is_technical", False)),
            )

            responses["success"].append({"row": row_data, "detail": "Club created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})