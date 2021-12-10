from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)

import jwt
from accounts.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('No token provided')

        token = auth_token[1]

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            email = payload['email']
            user = User.objects.get(email=email)
            return (user, token)
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is expired')
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is invalid')
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                'No such user')

        return super().authenticate(request)

    def authenticate_header(self, request):
        return 'Bearer'


class JWTAccountActivation():
    def generate_token(self, user):
        '''
        Generates a activation token for a user to have permissions.
        '''
        token = jwt.encode(
            {
                'email': user.email,
                'exp': datetime.utcnow()+timedelta(hours=1)
            },
            settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    def check_token(self, token):
        '''
        Checks if the activation token is valid. If its True, it returns the user model.
        '''
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            email = payload['email']
            user = User.objects.get(email=email)
            if user.is_active:
                raise exceptions.ParseError(
                    'Account already activated')
            return user
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.ParseError(
                'Token is expired')
        except jwt.DecodeError as ex:
            raise exceptions.ParseError(
                'Token is invalid')
        except User.DoesNotExist as no_user:
            raise exceptions.ParseError(
                'Token is invalid')


jwt_account_activation = JWTAccountActivation()
