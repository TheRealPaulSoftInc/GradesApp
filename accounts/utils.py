from accounts.jwt import jwt_account_activation
from django.conf import settings
from django.core.mail import send_mail


def send_activation_mail(user):
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
