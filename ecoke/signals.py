from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

from .models import Brand, Profile


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# @receiver(pre_save, sender=Brand)
# def validate_favourite_drink_choice(sender, instance, **kwargs):
#     valid_types = [t[1] for t in sender.DRINKS]
#     if instance.favourite_drink not in valid_types:
#         raise ValidationError(
#             'Brand favourite drink Type "{}" is not one of the \
#             permitted values'.format(instance.favourite_drink)
#         )

# This receiver handles token creation immediately a new user is created
# @receiver(post_save, sender=User)
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
@receiver(post_save, sender=get_user_model)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
