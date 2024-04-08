import io
import csv

from student_welfare_backend.users.models import User
from student_welfare_backend.core.models import Organization, Event, SpecialFile, Newsletter

CSV_TYPES = ["user", "Ooganization", "event","special_file","newsletter"]


USER_FIELDS = [
    "name",
    "email",
    "phone_no",
    "tenure",
    "verified",
    "is_faculty",
    "is_dsw",
    "is_adsw",
]

ORGANIZATION_FIELDS = [
    "name",
    "type",
    "sub_type",
    "logo_link",
]

EVENT_FIELDS = ["name", "description", "organization__name", "start_time", "end_time", "venue", "event_coordinators"]

SPECIALFILE_FIELDS = ["year", "file_link", "type"]

NEWSLETTER_FIELDS = ["link", "cover_page", "month", "year"]
# Create a csv in memory and return it as a file object
def write_csv(data, fields):
    csv_file = io.StringIO()
    print(clean_headers(fields))
    writer = csv.DictWriter(csv_file, fieldnames=clean_headers(fields))
    writer.writeheader()
    writer.writerows(data)
    # Reset the file pointer to the beginning of the file
    csv_file.seek(0)
    # Return the file object
    return csv_file


# Clean out headers for the csv file
def clean_headers(headers):
    return [header.replace("__", " ").replace("_", " ").title() for header in headers]


# Get the data from the model and return it as a list of dictionaries
def get_csv_data(model, filter, fields):
    def get_field_value(instance, field_name):
        if "__" in field_name:
            # Split the field name to get the related field and attribute
            related_field, related_attr = field_name.split("__")
            # Traverse the relationship and get the value of the related attribute
            related_obj = getattr(instance, related_field)
            if related_obj:
                # Recursively fetch the attribute value for nested related objects
                return get_field_value(related_obj, related_attr)
            else:
                return None
        else:
            # For non-related fields, directly get the attribute value
            return getattr(instance, field_name)

    # Get the data from the model
    data_models = model.objects.filter(**filter).all()
    # Get the data in the form of a dictionary. The fields should be in the form `object.field`
    data = []
    for data_model in data_models:
        data_entry = {}
        for field in fields:
            data_entry[
                clean_headers(
                    [
                        field,
                    ]
                )[0]
            ] = get_field_value(data_model, field)
        data.append(data_entry)
    return data


class CSVExporter:
    def __init__(self, csv_type):
        if csv_type not in CSV_TYPES:
            raise ValueError(f"Invalid CSV type '{csv_type}'")

        if csv_type == "user":
            self.csv_fields = USER_FIELDS
            self.model = User
        elif csv_type == "Ooganization":
            self.csv_fields = ORGANIZATION_FIELDS
            self.model = Organization
        elif csv_type == "event":
            self.csv_fields = EVENT_FIELDS
            self.model = Event
        elif csv_type == "special_file":
            self.csv_fields = SPECIALFILE_FIELDS
            self.model = SpecialFile
        elif csv_type == "newsletter":
            self.csv_fields = NEWSLETTER_FIELDS
            self.model = Newsletter

    def export_csv(self, filter):
        try:
            data = get_csv_data(self.model, filter, self.csv_fields)
        except Exception as e:
            return {"detail": str(e)}

        return write_csv(data, self.csv_fields)
