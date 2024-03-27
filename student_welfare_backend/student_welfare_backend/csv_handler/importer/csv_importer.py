
from student_welfare_backend.users.models import User
from student_welfare_backend.csv_handler.importer.organizations import OrganizationsCSVImporter
from student_welfare_backend.csv_handler.importer.events import EventsCSVImporter
from student_welfare_backend.csv_handler.importer.users import UsersCSVImporter
from student_welfare_backend.csv_handler.importer.newsletters import NewslettersCSVImporter
from student_welfare_backend.csv_handler.importer.special_files import SpecialFilesCSVImporter
from student_welfare_backend.csv_handler.importer.utils import process_csv


CSV_TYPES = {
    "organization": OrganizationsCSVImporter,
    "event": EventsCSVImporter,
    "user": UsersCSVImporter,
    "newsletter": NewslettersCSVImporter,
    "special_file": SpecialFilesCSVImporter,
}


class CSVImporter:
    def __init__(self, csv_type):
        if csv_type not in CSV_TYPES:
            raise ValueError(f"Invalid CSV type '{csv_type}'")
        
        self.importer = CSV_TYPES[csv_type]()

    def process_csv(self, file):
        return process_csv(file, 
                           self.importer.REQUIRED_FIELDS, 
                           self.importer.STANDARD_FIELDS, 
                           self.importer.process_csv_func)


