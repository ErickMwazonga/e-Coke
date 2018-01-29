from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email_unique(value):
    exists = User.objects.filter(email__iexact=value)

    if exists:
        raise ValidationError('The email address is already taken, \
                                Please try another')


def validate_username_unique(value):
    exists = User.objects.filter(username__iexact=value)
    invalid_usernames = [
        'abc',
        'me',
        'ecoke',
        'admin',
        'help',
        'helpdesk',
        'sales',
        'support',
        'info',
        'warning',
        'success',
        'danger',
        'error',
        'debug',
        'alert',
        'alerts',
        'signup',
        'signin',
        'signout',
        'login',
        'logout',
        'activate',
        'register',
        'password',
    ]
    if exists:
        raise ValidationError('This username is already taken, \
                                Please try another')
    elif value in invalid_usernames:
        raise ValidationError('This username is not allowed, \
                                Please try another')
