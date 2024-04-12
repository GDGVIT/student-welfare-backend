from student_welfare_backend.users.models import User
from student_welfare_backend.core.models import UserOrganizationRelation, Organization

class UsersCSVImporter:
    STANDARD_FIELDS = [
        "reg_no", 
        "name", 
        "email", 
        "phone", 
        "is_faculty",
        "tenure",
        "type",
        "role"
        ]
    REQUIRED_FIELDS = [
        "reg_no", 
        "name", 
        "email", 
        "phone",
        "type",
        "role"
        ]

    def process_csv_func(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.REQUIRED_FIELDS if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create user
            user,created = User.objects.update_or_create(
                username=row_data["reg_no"],
                defaults={
                    "name": row_data["name"],
                    "email": row_data["email"],
                    "phone_no": row_data["phone"],
                    "is_faculty": bool(row_data.get("is_faculty", False)),
                    "tenure": row_data.get("tenure", "")
                }
            )
            if created == True:
                user.set_unusable_password()
            user.save()
            #responses["success"].append({"row": row_data, "detail": "User created successfully"})
            organization_type = row_data["type"]
            organization = Organization.objects.get(type=organization_type)
            userrel= UserOrganizationRelation.objects.update_or_create(
                user=user,
                organization=organization,
                defaults={
                    "role": row_data["role"],
                },
            )
            responses["success"].append({"row": row_data, "detail": "User Organization Relation created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})