from django.core.management.base import BaseCommand
from student_welfare_backend.core.utils.notifications import send_notification


class Command(BaseCommand):
    help = "Pushes notifications to all users"

    def handle(self, *args, **kwargs):
        title = input("Enter title: ")
        body = input("Enter body: ")
        topic = input("Enter topic: ")
        image_url = input("Enter image url: ")
        send_notification(title, body, topic, image_url)
