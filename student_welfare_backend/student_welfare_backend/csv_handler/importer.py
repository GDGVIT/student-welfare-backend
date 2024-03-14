import csv
from datetime import datetime

from student_welfare_backend.users.models import User
from student_welfare_backend.core.models import Club, Event

CSV_TYPES = ["user", "club", "event"]

USER_CSV_STANDARD_FIELDS = ["reg_no", "name", "email", "phone", "is_faculty"]

USER_CSV_REQUIRED_FIELDS = ["reg_no", "name", "email", "phone"]

CLUB_CSV_STANDARD_FIELDS = ["name", "is_chapter", "is_technical"]

CLUB_CSV_REQUIRED_FIELDS = ["name"]

EVENT_CSV_STANDARD_FIELDS = [
    "name",
    "description",
    "club",
    "start_time",
    "end_time",
    "venue",
    "coordinator1",
    "coordinator2",
    "status",
]

EVENT_CSV_REQUIRED_FIELDS = [
    "name",
    "description",
    "club",
    "start_time",
    "end_time",
    "venue",
    "coordinator1",
    "status",
]



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


class CSVImporter:
    def __init__(self, csv_type):
        if csv_type not in CSV_TYPES:
            raise ValueError(f"Invalid CSV type '{csv_type}'")
        
        if csv_type == "user":
            self.required_columns = USER_CSV_REQUIRED_FIELDS
            self.columns = USER_CSV_STANDARD_FIELDS
            self.process_data_func = self.create_user_from_csv

        elif csv_type == "club":
            self.required_columns = CLUB_CSV_REQUIRED_FIELDS
            self.columns = CLUB_CSV_STANDARD_FIELDS
            self.process_data_func = self.create_club_from_csv

        elif csv_type == "event":
            self.required_columns = EVENT_CSV_REQUIRED_FIELDS
            self.columns = EVENT_CSV_STANDARD_FIELDS
            self.process_data_func = self.create_event_from_csv

    def create_user_from_csv(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.required_columns if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create user
            user = User.objects.create(
                username=row_data["reg_no"],
                name=row_data["name"],
                email=row_data["email"],
                phone_no=row_data["phone"],
                is_faculty=bool(row_data.get("is_faculty", False))
            )
            user.set_unusable_password()

            responses["success"].append({"row": row_data, "detail": "User created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})

    def create_club_from_csv(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.required_columns if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create club
            club = Club.objects.create(
                name=row_data["name"],
                is_chapter=bool(row_data.get("is_chapter", False)),
                is_technical=bool(row_data.get("is_technical", False))
            )

            responses["success"].append({"row": row_data, "detail": "Club created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})

    def create_event_from_csv(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.required_columns if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create event
            event = Event.objects.create(
                name=row_data["name"],
                description=row_data["description"],
                organizing_body=row_data["club"],
                start_time=datetime.strptime(row_data["start_time"], "%Y-%m-%d %H:%M:%S"),
                end_time=datetime.strptime(row_data["end_time"], "%Y-%m-%d %H:%M:%S"),
                venue=row_data["venue"],
                status=row_data["status"],
            )

            if row_data["coordinator1"]:
                event.event_coordinators.append(row_data["coordinator1"])
            if row_data["coordinator2"]:
                event.event_coordinators.append(row_data["coordinator2"])

            responses["success"].append({"row": row_data, "detail": "Event created successfully"})
        except Exception as e:
            responses["failure"].append({"row": row_data, "detail": str(e)})

    def process_csv(self, file):
        return process_csv(file, self.required_columns, self.columns, self.process_data_func)
