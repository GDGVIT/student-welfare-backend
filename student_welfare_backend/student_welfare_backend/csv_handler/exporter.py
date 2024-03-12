import io
import csv

from student_welfare_backend.users.models import User
from student_welfare_backend.core.models import Club, Event
from student_welfare_backend.users.models import User
from student_welfare_backend.core.models import Club, Event

CSV_TYPES = ["user", "club", "event"]


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



# Create a csv in memory and return it as a file object
def write_csv(data, fields):
    csv_file = io.StringIO()
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)
    # Reset the file pointer to the beginning of the file
    csv_file.seek(0)
    # Return the file object
    return csv_file

def get_csv_data(model, filter, fields):
    # Get the data from the model
    data_models = model.objects.filter(**filter).all()
    # Get the data in the form of a dictionary. The fields should be in the form `object.field`
    data = []
    for data_model in data_models:
        data.append({field: getattr(data_model, field) for field in fields})
    return data


class CSVExporter:

    def __init__(self, csv_type):
        if csv_type not in CSV_TYPES:
            raise ValueError(f"Invalid CSV type '{csv_type}'")
        
        if csv_type == "user":
            self.csv_fields = USER_FIELDS
            self.model = User


    def export_csv(self, filter):
        try:
            data = get_csv_data(self.model, filter, self.csv_fields)
        except Exception as e:
            return {"detail": str(e)}

        return write_csv(data, self.csv_fields)

    



