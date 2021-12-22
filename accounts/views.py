from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import Http404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.jwt import jwt_account_activation
from accounts.models import User
from accounts.serializers import LoginSerializer, UserSerializer


class RegisterView(GenericAPIView):

    authentication_classes = []
    serializer_class = UserSerializer

    def _send_activation_mail(self, request, user):
        token = jwt_account_activation.generate_token(user)
        activation_link = settings.EMAIL_VERIFICATION_URL + token
        target_email = user.email
        send_mail(
            subject='Account activation',
            message=f'Activate your account here: {activation_link}',
            from_email=None,
            recipient_list=[target_email],
            fail_silently=False,
        )

    def post(self, request):
        """
        Register a new User.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # TODO: Implemented asyncronous call
            try:
                self._send_activation_mail(request, user)
            except Exception:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):

    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Retrieve auth token by providing credentials
        """
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(
            username=email, password=password)

        if user and user.is_active:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user and not user.is_active:
            return Response({'message': "Inactive account. Activate your account via email"}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserAuthView(GenericAPIView):

    def get(self, request):
        """
        Retrieve the logged user
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ActivationView(APIView):

    authentication_classes = []

    def put(self, request, token):
        """
        Activate an account via a token
        """
        user = jwt_account_activation.check_token(token)
        if user:
            user.is_active = True
            user.save()
            return Response({'message': "User account succesfully activated"}, status=status.HTTP_201_CREATED)
        return Response({'message': "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# Only for admins
class UserDetailView(RetrieveUpdateDestroyAPIView):
    """
    get: Retrieves a User by Id
    put: Updates a User by Id
    delete: Deletes a User by Id
    """

    http_method_names = ['get', 'put', 'delete']
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, DjangoModelPermissions]
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.all()


# Only for admins
class UserListView(ListAPIView):
    """
    get: Retrieves a List of Users
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ['id']

    def get_queryset(self):
        return User.objects.all()
