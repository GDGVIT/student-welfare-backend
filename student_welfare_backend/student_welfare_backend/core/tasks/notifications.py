import firebase_admin
from firebase_admin import messaging, credentials
from config.celery_app import app
from django.utils import timezone
import logging
from student_welfare_backend.core.models import Event
from django.contrib.auth import get_user_model


cred = credentials.Certificate("/app/credentials/firebase-key.json")
firebase_app = firebase_admin.initialize_app(cred)

print("Firebase app initialized.", firebase_app)

def get_title(event: Event):
    return f"Register for {event.name} by {event.organization.name} on VTOP now!"


@app.task(name="send_notification")
def send_notification(title, body, topic=None, image_url=None):
    User = get_user_model()
    tokens = User.objects.exclude(fcm_token__isnull=True).exclude(fcm_token="").values_list("fcm_token", flat=True)
    tokens = list(tokens)
    if not tokens:
        print("No user tokens available.")
        return

    notification = messaging.Notification(
        title=title,
        body=body,
        image=image_url
    )

    if topic:
        topic = f"/topics/{topic.replace(' ', '_').lower()}"
        message = messaging.Message(
            notification=notification,
            topic=topic,
        )
        try:
            response = messaging.send(message)
            print(f"Successfully sent message to topic {topic}: {response}")
        except Exception as e:
            logging.error(f"Error sending message to topic {topic}: {e}")

    failed_tokens = []
    for token in tokens:
        message = messaging.Message(
            notification=notification,
            token=token,
        )
        try:
            response = messaging.send(message)
            print(f"Successfully sent message to {token}: {response}")
        except Exception as e:
            logging.error(f"Error sending message to {token}: {e}")
            failed_tokens.append(token)

    if failed_tokens:
        print('List of tokens that caused failures: {0}'.format(failed_tokens))


@app.task(name="send_event_notification")
def send_event_notification(event: Event):
    title = get_title(event)
    topic = f"{event.organization.name}"
    image_url = event.poster_link
    body = event.description
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
