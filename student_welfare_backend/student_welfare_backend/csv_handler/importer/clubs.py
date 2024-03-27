from student_welfare_backend.core.models import Club


class ClubsCSVImporter:
    STANDARD_FIELDS = [
        "name", 
        "type", 
        "sub_type",
        "description",
        ]
    REQUIRED_FIELDS = ["name","type"]

    def process_csv_func(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.REQUIRED_FIELDS if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create club
            club = Club.objects.update_or_create(
                name=row_data["name"],
                defaults={
                    "type": row_data["type"],
                    "sub_type": row_data["sub_type"],
                    "description": row_data["description"]
                },
            )

            responses["success"].append({"row": row_data, "detail": "Club created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})