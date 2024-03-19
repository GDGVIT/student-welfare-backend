
from datetime import datetime

from student_welfare_backend.core.models import Event


class EventsCSVImporter:
    STANDARD_FIELDS = [
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
    REQUIRED_FIELDS = [
        "name",
        "description",
        "club",
        "start_time",
        "end_time",
        "venue",
        "status",
    ]

    def process_csv_func(self, row_data, responses):
        try:
            # Validate required fields
            missing_fields = [field for field in self.required_columns if row_data[field] is None]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create event
            event = Event.objects.update_or_create(
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