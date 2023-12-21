from rest_framework.views import APIView
from rest_framework.response import Response

from myapp.serializers import EmailSerializer
from myapp.serializers import CustomTokenObtainPairSerializer
from myapp.models import Contact

from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import threading

class HandleEmails(threading.Thread):
    def __init__(self, message, subject, recipient_email, html_message):
        self.message = message
        self.subject = subject
        self.recipient_email = recipient_email
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        from_email = 'thecontactpage@gmail.com'
        send_mail(self.subject, self.message, from_email, self.recipient_email, html_message=self.html_message, fail_silently=False)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class SendEmailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(f"Request URL: {self.request.build_absolute_uri()}")
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            content = serializer.validated_data['content']

            user_id = self.request.user.id
            emails = ['juliorwema@gmail.com', 'wlasounds@gmail.com', 'grogusix9@gmail.com']
            titles = ['WLIAN SOUNDS', 'BIG BIKERS', 'SLOPPY GANG']

            try:
                recipient_email = emails[user_id - 1]
                title = titles[user_id - 1]
            except IndexError:
                return Response({'error': 'Invalid user_id.'})

            print(f"Sending email to: {recipient_email}")
            print(f"Title is: {title}")
            try:
                validate_email(recipient_email)
            except ValidationError:
                return Response({'error': 'Invalid recipient email.'})

            html_message = render_to_string('new-email.html', {
                'name': name,
                'email': email,
                'content': content,
                'title': title
            })
            subject = 'Contact form submission'
            message = 'New message notification'

            HandleEmails(subject, message, [recipient_email], html_message=html_message).start()
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)