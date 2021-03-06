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
from rest_framework import authentication, permissions
# from rest_framework.response import Response
from api.serializers import ( RequestSerializer, 
                              RequestWriterSerializer, 
                              OrderSerializer, 
                              OrderWriterSerializer, 
                              ProductSerializer)
from rest_framework import viewsets
from core.models import Request, Order, Product
from rest_framework import status
from rest_framework.decorators import action
from datetime import datetime
from rest_framework.response import Response


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

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all() # TODO: show requests per user
    serializer_class = RequestSerializer
    write_serializer_class = RequestWriterSerializer
    pagination_class = None
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       permissions.IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.write_serializer_class
        return self.serializer_class



class TransportOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all() # TODO: Show this per user only
    serializer_class = OrderSerializer
    writer_serializer_class = OrderWriterSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'create':
            return self.writer_serializer_class
        return self.serializer_class


class ClientOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    writer_serializer_class = OrderWriterSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'create':
            return self.writer_serializer_class
        return self.serializer_class

    #Holder while updating login feature
    def get_queryset(self):
        return Order.objects.filter(request__user__id__exact=5).order_by('-request__end_date')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
