from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from student_welfare_backend.core.api.customs.permissions import IsDSW
from student_welfare_backend.core.utils.notifications import send_notification



class PushNotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW]

    def post(self, request):
        title = request.data.get("title")
        body = request.data.get("body")
        topic = request.data.get("topic")
        image_url = request.data.get("image_url", None)
        send_notification.delay(title, body, topic, image_url)
        return Response({"message": "Notification sent successfully"}, 
                        status=status.HTTP_200_OK)