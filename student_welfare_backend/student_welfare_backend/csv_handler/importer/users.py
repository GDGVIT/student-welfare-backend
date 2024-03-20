from student_welfare_backend.users.models import User


class UsersCSVImporter:
    STANDARD_FIELDS = [
        "reg_no", 
        "name", 
        "email", 
        "phone", 
        "is_faculty",
        "tenure",
        ]
    REQUIRED_FIELDS = [
        "reg_no", 
        "name", 
        "email", 
        "phone"
        ]

    def process_csv_func(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.required_columns if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create user
            user = User.objects.update_or_create(
                username=row_data["reg_no"],
                defaults={
                    "name": row_data["name"],
                    "email": row_data["email"],
                    "phone_no": row_data["phone"],
                    "is_faculty": bool(row_data.get("is_faculty", False)),
                    "tenure": row_data.get("tenure", ""),
                },
            )
            user.set_unusable_password()

            responses["success"].append({"row": row_data, "detail": "User created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})