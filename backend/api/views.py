from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import viewsets
from api.serializers import UserSerializer
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from django_rest_passwordreset.signals import reset_password_token_created


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class HelloView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        self.is_not_used()
        content = {'message': 'Hello World'}
        return Response(content)

    def is_not_used(self):
        pass


class PasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
        """
        Handles password reset tokens
        When a token is created, an e-mail needs to be sent to the user
        :param sender: View Class that sent the signal
        :param instance: View Instance that sent the signal
        :param reset_password_token: Token Model Object
        :param args:
        :param kwargs:
        :return:
        """
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
        }

        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {title}".format(title="Some website title"),
            # message:
            email_plaintext_message,
            # from:
            "noreply@somehost.local",
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
