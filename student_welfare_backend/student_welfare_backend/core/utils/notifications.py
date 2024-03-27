import firebase_admin
from firebase_admin import messaging, credentials
from config.celery_app import app
from django.utils import timezone

from student_welfare_backend.core.models import Event

cred = credentials.Certificate("/app/credentials/firebase-key.json")
firebase_app = firebase_admin.initialize_app(cred)


@app.task(name="send_notification")
def send_notification(title, body, topic, image_url=None):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body, image=image_url),
        topic=f"/topics/{topic.replace(' ', '_').lower()}",
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)


@app.task(name="send_event_notification")
def send_event_notification(event: Event, body: str):
    title = event.title
    topic = f"{event.organization.name}"
    image_url = event.poster_link
    send_notification(title, body, topic, image_url)


@app.task(name="daily_event_notification")
def daily_event_notification():
    events = Event.objects.filter(start_time__date=timezone.date.today())
    for event in events:
        send_event_notification.delay(event, "Event today!")


@app.task(name="event_start_notification")
def event_start_notification():
    events = Event.objects.filter(start_time__date=timezone.date.today(), start_time__hour=timezone.now().hour)
    for event in events:
        send_event_notification.delay(event, "Event started!")
